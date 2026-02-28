"""OpenStreetMap Overpass API connector."""

from typing import Any

import geopandas as gpd
from shapely.geometry import Point, Polygon

from citysense.connectors.base import BaseConnector
from citysense.geo.bbox import BBox
from citysense.geo.osm import build_bbox_query, overpass_query


class OSMConnector(BaseConnector):
    """OpenStreetMap Overpass API connector."""

    @property
    def source_id(self) -> str:
        return "osm"

    @property
    def license(self) -> str:
        return "ODbL 1.0"

    async def fetch(
        self,
        bbox: BBox,
        tags: list[tuple[str, str]] | None = None,
        **kwargs: Any,
    ) -> gpd.GeoDataFrame:
        """Fetch OSM features for bbox.

        Args:
            bbox: Bounding box.
            tags: OSM tag filters.

        Returns:
            GeoDataFrame with OSM features.
        """
        tags = tags or [("building", ""), ("amenity", "")]
        query = build_bbox_query(bbox.to_tuple(), tags)  # (west,south,east,north)
        data = await overpass_query(query)
        features = []
        for el in data.get("elements", []):
            if el.get("type") == "node":
                geom = Point(el["lon"], el["lat"])
            elif el.get("type") == "way" and "geometry" in el:
                coords = [(c["lon"], c["lat"]) for c in el["geometry"]]
                if len(coords) >= 3:
                    geom = Polygon(coords)
                else:
                    continue
            else:
                continue
            props = el.get("tags", {})
            features.append(
                {
                    "feature_id": f"osm:{el.get('id', '')}",
                    "geometry": geom,
                    "country": kwargs.get("country", ""),
                    "feature_type": list(props.keys())[0] if props else "unknown",
                    "feature_subtype": list(props.values())[0] if props else "",
                    "properties": props,
                    "source_id": self.source_id,
                }
            )
        if not features:
            return gpd.GeoDataFrame(columns=["feature_id", "geometry", "source_id"])
        gdf = gpd.GeoDataFrame(features, crs="EPSG:4326")
        return gdf

    async def health_check(self) -> bool:
        """Check Overpass API availability."""
        try:
            data = await overpass_query("[out:json];node(1);out;")
            return "elements" in data
        except Exception:
            return False
