"""Copernicus Data Space Ecosystem (CDSE) STAC connector.

Collections: SENTINEL-2-L2A, SENTINEL-1-GRD
Authentication: OAuth2 client credentials.
"""

from datetime import datetime
from typing import TYPE_CHECKING, Any

import httpx
import pystac_client
from pystac_client import Client

from citysense.connectors.base import BaseConnector

if TYPE_CHECKING:
    pass
from citysense.core.exceptions import CDSEAuthError
from citysense.geo.bbox import BBox

CDSE_AUTH_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
)


class SentinelConnector(BaseConnector):
    """CDSE STAC connector for Sentinel-2 and Sentinel-1."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        stac_url: str = "https://stac.dataspace.copernicus.eu",
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._stac_url = stac_url
        self._token: str | None = None
        self._token_expires: datetime | None = None

    @property
    def source_id(self) -> str:
        return "cdse_sentinel2"

    @property
    def license(self) -> str:
        return "Copernicus Open Access"

    async def _get_token(self) -> str:
        if self._token and self._token_expires and datetime.utcnow() < self._token_expires:
            return self._token
        if not self._client_id or not self._client_secret:
            raise CDSEAuthError("CDSE client_id and client_secret required")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                CDSE_AUTH_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30.0,
            )
            if response.status_code != 200:
                raise CDSEAuthError(f"CDSE auth failed: {response.status_code}")
            data = response.json()
        self._token = data["access_token"]
        expires_in = data.get("expires_in", 600)
        from datetime import timedelta

        self._token_expires = datetime.utcnow() + timedelta(seconds=expires_in - 60)
        return self._token

    async def search(
        self,
        bbox: BBox,
        collection: str = "SENTINEL-2-L2A",
        datetime_range: str | None = None,
        max_cloud_cover: float = 20.0,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """Search CDSE STAC for scenes.

        Args:
            bbox: Bounding box.
            collection: SENTINEL-2-L2A or SENTINEL-1-GRD.
            datetime_range: ISO 8601 range, e.g. 2024-01-01/2024-12-31.
            max_cloud_cover: Max cloud cover for Sentinel-2.
            limit: Max results.

        Returns:
            List of scene metadata dicts.
        """
        await self._get_token()
        catalog = pystac_client.Client.open(
            self._stac_url,
            headers={"Authorization": f"Bearer {self._token}"},
        )
        bbox_list = [bbox.west, bbox.south, bbox.east, bbox.north]
        search = catalog.search(
            collections=[collection],
            bbox=bbox_list,
            datetime=datetime_range,
        )
        if collection == "SENTINEL-2-L2A":
            search = search.filter("lte", "eo:cloud_cover", max_cloud_cover)
        items = list(search.items())[:limit]
        return [
            {
                "id": item.id,
                "datetime": str(item.datetime) if item.datetime else "",
                "bbox": item.bbox,
                "geometry": item.geometry,
                "assets": list(item.assets.keys()),
                "cloud_cover": item.extra.get("eo:cloud_cover"),
            }
            for item in items
        ]

    async def fetch(
        self,
        bbox: BBox,
        collection: str = "SENTINEL-2-L2A",
        datetime_range: str | None = None,
        **kwargs: Any,
    ) -> Any:
        """Fetch scene metadata as GeoDataFrame.

        Returns scene footprints, not raster data. Use imagery.satellite
        for actual band download and processing.
        """
        import geopandas as gpd
        from shapely.geometry import shape

        scenes = await self.search(
            bbox=bbox,
            collection=collection,
            datetime_range=datetime_range,
            **kwargs,
        )
        features = []
        for s in scenes:
            geom = s.get("geometry")
            if geom:
                features.append(
                    {
                        "feature_id": f"cdse:{s['id']}",
                        "geometry": shape(geom),
                        "country": kwargs.get("country", ""),
                        "feature_type": "satellite_scene",
                        "feature_subtype": collection,
                        "properties": {
                            "datetime": s.get("datetime"),
                            "cloud_cover": s.get("cloud_cover"),
                            "assets": s.get("assets", []),
                        },
                        "source_id": self.source_id,
                    }
                )
        if not features:
            return gpd.GeoDataFrame(columns=["feature_id", "geometry", "source_id"])
        return gpd.GeoDataFrame(features, crs="EPSG:4326")

    async def health_check(self) -> bool:
        """Check CDSE STAC availability."""
        try:
            catalog = Client.open(self._stac_url)
            _ = list(catalog.get_collections())[:1]
            return True
        except Exception:
            return False
