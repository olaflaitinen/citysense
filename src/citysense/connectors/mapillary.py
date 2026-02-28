"""Mapillary Graph API v4 connector.

Endpoint: https://graph.mapillary.com/images
Bbox constraint: area must be smaller than 0.01 degrees square.
Bbox format: left, bottom, right, top (minLon, minLat, maxLon, maxLat).
"""

from datetime import datetime
from typing import Any

import geopandas as gpd
import httpx
from shapely.geometry import Point

from citysense.connectors.base import BaseConnector
from citysense.core.exceptions import ConnectorAuthError, MapillaryQuotaError
from citysense.geo.bbox import BBox

MAPILLARY_IMAGES_URL = "https://graph.mapillary.com/images"
MAPILLARY_BBOX_MAX_AREA_DEG2 = 0.01


class MapillaryConnector(BaseConnector):
    """Mapillary Graph API v4 connector for street-level imagery."""

    def __init__(self, access_token: str | None = None) -> None:
        """Initialise with access token.

        Args:
            access_token: Mapillary client access token from
                https://www.mapillary.com/dashboard/developers
        """
        self._token = access_token

    @property
    def source_id(self) -> str:
        return "mapillary_v4"

    @property
    def license(self) -> str:
        return "CC BY-SA 4.0"

    def _check_token(self) -> None:
        if not self._token:
            raise ConnectorAuthError("Mapillary access token required")

    def _bbox_area_deg2(self, bbox: BBox) -> float:
        return (bbox.east - bbox.west) * (bbox.north - bbox.south)

    async def fetch(
        self,
        bbox: BBox,
        fields: str = (
            "id,captured_at,thumb_1024_url,thumb_2048_url,geometry,compass_angle,sequence_id"
        ),
        limit: int = 50,
        start_captured_at: str | None = None,
        **kwargs: Any,
    ) -> gpd.GeoDataFrame:
        """Fetch Mapillary images within bbox.

        Bbox area must be smaller than 0.01 deg^2. For larger areas,
        split the bbox or use mapillary-python-sdk.

        Args:
            bbox: Bounding box (west, south, east, north).
            fields: Comma-separated field list.
            limit: Max images (max 2000).
            start_captured_at: ISO 8601 filter for minimum capture date.

        Returns:
            GeoDataFrame with image metadata and Point geometry.
        """
        self._check_token()
        assert self._token is not None
        area = self._bbox_area_deg2(bbox)
        if area > MAPILLARY_BBOX_MAX_AREA_DEG2:
            return await self._fetch_tiled(bbox, fields, limit, start_captured_at)
        bbox_str = f"{bbox.west},{bbox.south},{bbox.east},{bbox.north}"
        params: dict[str, str | int] = {
            "access_token": self._token,
            "fields": fields,
            "bbox": bbox_str,
            "limit": min(limit, 2000),
        }
        if start_captured_at:
            params["start_captured_at"] = start_captured_at
        async with httpx.AsyncClient() as client:
            response = await client.get(MAPILLARY_IMAGES_URL, params=params, timeout=30.0)
            if response.status_code == 401:
                raise ConnectorAuthError("Invalid Mapillary access token")
            if response.status_code == 429:
                raise MapillaryQuotaError("Mapillary API rate limit exceeded")
            response.raise_for_status()
            data = response.json()
        features = self._parse_response(data, kwargs.get("country", ""))
        if not features:
            return gpd.GeoDataFrame(columns=["feature_id", "geometry", "source_id"])
        return gpd.GeoDataFrame(features, crs="EPSG:4326")

    async def _fetch_tiled(
        self,
        bbox: BBox,
        fields: str,
        limit: int,
        start_captured_at: str | None,
    ) -> gpd.GeoDataFrame:
        """Fetch by splitting bbox into sub-boxes under 0.01 deg^2."""
        sub_boxes: list[BBox] = []
        cell_side = 0.05
        lon = bbox.west
        while lon < bbox.east:
            lat = bbox.south
            while lat < bbox.north:
                e = min(lon + cell_side, bbox.east)
                n = min(lat + cell_side, bbox.north)
                sub = BBox(west=lon, south=lat, east=e, north=n)
                if self._bbox_area_deg2(sub) <= MAPILLARY_BBOX_MAX_AREA_DEG2:
                    sub_boxes.append(sub)
                lat = n
            lon += cell_side
        all_features: list[dict[str, Any]] = []
        seen_ids: set[str] = set()
        for sub in sub_boxes[:20]:
            if len(all_features) >= limit:
                break
            gdf = await self.fetch(
                sub,
                fields=fields,
                limit=limit - len(all_features),
                start_captured_at=start_captured_at,
            )
            for _, row in gdf.iterrows():
                fid = row.get("feature_id", "")
                if fid and fid not in seen_ids:
                    seen_ids.add(fid)
                    all_features.append(row.to_dict())
        if not all_features:
            return gpd.GeoDataFrame(columns=["feature_id", "geometry", "source_id"])
        return gpd.GeoDataFrame(all_features, crs="EPSG:4326")

    def _parse_response(self, data: dict[str, Any], country: str) -> list[dict[str, Any]]:
        features: list[dict[str, Any]] = []
        for item in data.get("data", []):
            geom = item.get("geometry") or item.get("computed_geometry")
            if not geom or geom.get("type") != "Point":
                continue
            coords = geom.get("coordinates", [0, 0])
            point = Point(coords[0], coords[1])
            captured = item.get("captured_at")
            if isinstance(captured, (int, float)):
                captured_dt = datetime.utcfromtimestamp(captured / 1000).isoformat() + "Z"
            else:
                captured_dt = str(captured) if captured else ""
            features.append(
                {
                    "feature_id": f"mapillary:{item.get('id', '')}",
                    "geometry": point,
                    "country": country,
                    "feature_type": "street_imagery",
                    "feature_subtype": "mapillary",
                    "properties": {
                        "captured_at": captured_dt,
                        "thumb_1024_url": item.get("thumb_1024_url"),
                        "thumb_2048_url": item.get("thumb_2048_url"),
                        "compass_angle": item.get("compass_angle"),
                        "sequence_id": item.get("sequence_id"),
                    },
                    "source_id": self.source_id,
                }
            )
        return features

    async def health_check(self) -> bool:
        """Check Mapillary API availability."""
        self._check_token()
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    MAPILLARY_IMAGES_URL,
                    params={"access_token": self._token, "fields": "id", "limit": 1},
                    timeout=10.0,
                )
                return r.status_code == 200
        except Exception:
            return False
