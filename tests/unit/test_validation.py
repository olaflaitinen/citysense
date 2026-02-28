"""Unit tests for GeoJSON validators."""

import pytest

from citysense.utils.validation import GeoJSONGeometry


def test_geojson_point() -> None:
    """Test valid Point geometry."""
    g = GeoJSONGeometry(type="Point", coordinates=[24.9, 60.1])
    assert g.type == "Point"
    assert g.coordinates == [24.9, 60.1]


def test_geojson_polygon() -> None:
    """Test valid Polygon geometry."""
    coords = [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
    g = GeoJSONGeometry(type="Polygon", coordinates=coords)
    assert g.type == "Polygon"


def test_geojson_all_types() -> None:
    """Test all allowed geometry types."""
    for t in ("LineString", "MultiPoint", "MultiLineString", "MultiPolygon"):
        g = GeoJSONGeometry(type=t, coordinates=[])
        assert g.type == t


def test_geojson_invalid_type() -> None:
    """Test invalid geometry type raises."""
    with pytest.raises(ValueError, match="Invalid geometry type"):
        GeoJSONGeometry(type="Invalid", coordinates=[])
