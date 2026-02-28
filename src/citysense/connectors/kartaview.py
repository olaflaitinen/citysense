"""KartaView REST API connector.

Endpoint: https://kartaview.org/api/1.0/list/nearby-photos/
No authentication required for public reads.
"""

import math
from typing import Any

import geopandas as gpd
import httpx
from shapely.geometry import Point

from citysense.connectors.base import BaseConnector
from citysense.geo.bbox import BBox

KARTAVIEW_BASE = "https://kartaview.org/api"
KARTAVIEW_NEARBY_URL = f"{KARTAVIEW_BASE}/1.0/list/nearby-photos/"


class KartaViewConnector(BaseConnector):
    """KartaView REST API connector for street-level imagery."""

    def __init__(self, base_url: str = KARTAVIEW_BASE) -> None:
        self._base = base_url.rstrip("/")
        self._nearby_url = f"{self._base}/1.0/list/nearby-photos/"

    @property
    def source_id(self) -> str:
        return "kartatview"

    @property
    def license(self) -> str:
        return "CC BY-SA 4.0"

    def _bbox_to_center_radius(self, bbox: BBox) -> tuple[float, float, float]:
        lat = (bbox.south + bbox.north) / 2
        lon = (bbox.west + bbox.east) / 2
        lon_deg_m = 111320 * abs(math.cos(math.radians(lat)))
        radius_m = (
            max(
                abs(bbox.north - bbox.south) * 111320,
                abs(bbox.east - bbox.west) * lon_deg_m,
            )
            / 2
        )
        return lat, lon, max(radius_m, 100)

    async def fetch(
        self,
        bbox: BBox,
        page: int = 1,
        ipp: int = 100,
        **kwargs: Any,
    ) -> gpd.GeoDataFrame:
        """Fetch KartaView photos near bbox centre.

        Args:
            bbox: Bounding box.
            page: Page number.
            ipp: Items per page (max 100).

        Returns:
            GeoDataFrame with photo metadata.
        """
        lat, lon, radius = self._bbox_to_center_radius(bbox)
        params: dict[str, float | int] = {
            "lat": lat,
            "lng": lon,
            "radius": int(radius),
            "page": page,
            "ipp": min(ipp, 100),
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(self._nearby_url, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
        features = self._parse_response(data, bbox, kwargs.get("country", ""))
        if not features:
            return gpd.GeoDataFrame(columns=["feature_id", "geometry", "source_id"])
        return gpd.GeoDataFrame(features, crs="EPSG:4326")

    def _parse_response(
        self, data: dict[str, Any], bbox: BBox, country: str
    ) -> list[dict[str, Any]]:
        features: list[dict[str, Any]] = []
        result: dict[str, Any] = (
            data.get("result", data) if isinstance(data, dict) else dict[str, Any]()
        )
        photos = result.get("photos", result.get("data", []))
        if isinstance(photos, dict):
            photos = photos.get("items", [])
        for item in photos if isinstance(photos, list) else []:
            if "lng" in item and "lat" in item:
                lat, lng = float(item["lat"]), float(item["lng"])
            elif "latitude" in item and "longitude" in item:
                lat, lng = float(item["latitude"]), float(item["longitude"])
            else:
                continue
            if not (bbox.south <= lat <= bbox.north and bbox.west <= lng <= bbox.east):
                continue
            pid = item.get("id", item.get("sequence_index", item.get("photo_id", "")))
            features.append(
                {
                    "feature_id": f"kartatview:{pid}",
                    "geometry": Point(lng, lat),
                    "country": country,
                    "feature_type": "street_imagery",
                    "feature_subtype": "kartatview",
                    "properties": {
                        "sequence_id": item.get("sequence_id"),
                        "captured_at": item.get("captured_at", item.get("create_time")),
                        "url": item.get("url", item.get("image_url", item.get("lth_name"))),
                    },
                    "source_id": self.source_id,
                }
            )
        return features

    async def health_check(self) -> bool:
        """Check KartaView API availability."""
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    self._nearby_url,
                    params={"lat": 60.17, "lng": 24.94, "radius": 100, "ipp": 1},
                    timeout=10.0,
                )
                return r.status_code == 200
        except Exception:
            return False
