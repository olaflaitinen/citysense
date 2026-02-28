"""H3 hexagonal indexing via h3-py 4.x.

H3 4.x API mapping:
- h3.polyfill -> h3.polygon_to_cells
- h3.h3_to_geo -> h3.cell_to_latlng

Approximate cell areas:
$A_9 \\approx 0.1052 \\, \\text{km}^2$, $A_7 \\approx 5.1613 \\, \\text{km}^2$

$$A_r = \\frac{A_{\\text{earth}}}{20 \\cdot 7^r} \\cdot k$$
"""

from typing import Any

import h3
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry

from citysense.geo.bbox import BBox


def polyfill(geometry: BaseGeometry | dict[str, Any], resolution: int) -> frozenset[str]:
    """Fill geometry with H3 cells at given resolution.

    Args:
        geometry: Shapely Polygon or GeoJSON dict (coordinates [lon, lat]).
        resolution: H3 resolution (0-15).

    Returns:
        Frozenset of H3 cell indices.
    """
    if isinstance(geometry, dict):
        geojson = geometry
    else:
        from shapely.geometry import mapping

        geojson = mapping(geometry)
    if geojson.get("type") != "Polygon":
        geom = shape(geojson)
        geojson = {"type": "Polygon", "coordinates": [list(geom.convex_hull.exterior.coords)]}
    if hasattr(h3, "geo_to_cells"):
        cells = h3.geo_to_cells(geojson, resolution)
    elif hasattr(h3, "polygon_to_cells"):
        cells = h3.polygon_to_cells(geojson, resolution)
    else:
        cells = h3.polyfill(geojson, resolution)
    return frozenset(cells)


def k_ring_buffer(h3_index: str, k: int) -> frozenset[str]:
    """Get k-ring neighbourhood of H3 cell.

    Args:
        h3_index: H3 cell index.
        k: Ring radius.

    Returns:
        Frozenset of H3 cell indices in k-ring.
    """
    if hasattr(h3, "grid_disk"):
        return frozenset(h3.grid_disk(h3_index, k))
    return frozenset(h3.k_ring(h3_index, k))


def compact(h3_set: frozenset[str]) -> frozenset[str]:
    """Compact a set of H3 cells to parent resolution where possible.

    Args:
        h3_set: Set of H3 cell indices.

    Returns:
        Compacted frozenset.
    """
    if hasattr(h3, "compact_cells"):
        return frozenset(h3.compact_cells(h3_set))
    return frozenset(h3.compact(h3_set))


def h3_to_centroid(h3_index: str) -> tuple[float, float]:
    """Get centroid (lat, lon) of H3 cell.

    Args:
        h3_index: H3 cell index.

    Returns:
        (latitude, longitude) tuple.
    """
    if hasattr(h3, "cell_to_latlng"):
        lat, lon = h3.cell_to_latlng(h3_index)
    else:
        lat, lon = h3.h3_to_geo(h3_index)
    return (lat, lon)


def bbox_to_h3_set(bbox: BBox, resolution: int) -> frozenset[str]:
    """Convert bounding box to H3 cell set.

    Args:
        bbox: Bounding box in EPSG:4326.
        resolution: H3 resolution.

    Returns:
        Frozenset of H3 cell indices covering bbox.
    """
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [bbox.west, bbox.south],
                [bbox.east, bbox.south],
                [bbox.east, bbox.north],
                [bbox.west, bbox.north],
                [bbox.west, bbox.south],
            ]
        ],
    }
    if hasattr(h3, "geo_to_cells"):
        cells = h3.geo_to_cells(geojson, resolution)
    elif hasattr(h3, "polygon_to_cells"):
        cells = h3.polygon_to_cells(geojson, resolution)
    else:
        cells = h3.polyfill(geojson, resolution)
    return frozenset(cells)
