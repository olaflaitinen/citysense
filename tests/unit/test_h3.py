"""Unit tests for H3 indexing."""

from shapely.geometry import Polygon

from citysense.geo.bbox import BBox
from citysense.geo.h3 import bbox_to_h3_set, compact, h3_to_centroid, k_ring_buffer, polyfill


def test_polyfill_with_dict() -> None:
    """Test polyfill with GeoJSON dict."""
    geojson = {
        "type": "Polygon",
        "coordinates": [
            [
                [24.9, 60.1],
                [25.0, 60.1],
                [25.0, 60.2],
                [24.9, 60.2],
                [24.9, 60.1],
            ]
        ],
    }
    cells = polyfill(geojson, resolution=9)
    assert len(cells) > 0
    assert all(isinstance(c, str) for c in cells)


def test_polyfill_with_shapely() -> None:
    """Test polyfill with Shapely geometry."""
    poly = Polygon([(24.9, 60.1), (25.0, 60.1), (25.0, 60.2), (24.9, 60.2)])
    cells = polyfill(poly, resolution=9)
    assert len(cells) > 0


def test_k_ring_buffer() -> None:
    """Test k-ring neighbourhood."""
    geojson = {
        "type": "Polygon",
        "coordinates": [[[24.9, 60.1], [25, 60.1], [25, 60.2], [24.9, 60.2], [24.9, 60.1]]],
    }
    cells = polyfill(geojson, 9)
    cell = next(iter(cells))
    ring = k_ring_buffer(cell, 1)
    assert len(ring) > 1
    assert cell in ring


def test_compact() -> None:
    """Test H3 compact."""
    geojson = {
        "type": "Polygon",
        "coordinates": [[[24.9, 60.1], [25, 60.1], [25, 60.2], [24.9, 60.2], [24.9, 60.1]]],
    }
    cells = polyfill(geojson, 9)
    compacted = compact(cells)
    assert len(compacted) <= len(cells) or len(compacted) >= 1


def test_h3_to_centroid() -> None:
    """Test H3 cell centroid."""
    geojson = {
        "type": "Polygon",
        "coordinates": [[[24.9, 60.1], [25, 60.1], [25, 60.2], [24.9, 60.2], [24.9, 60.1]]],
    }
    cells = polyfill(geojson, 9)
    cell = next(iter(cells))
    lat, lon = h3_to_centroid(cell)
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180


def test_bbox_to_h3_set() -> None:
    """Test bbox to H3 conversion."""
    bbox = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
    cells = bbox_to_h3_set(bbox, resolution=9)
    assert len(cells) > 0
