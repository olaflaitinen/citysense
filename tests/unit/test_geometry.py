"""Unit tests for geometry operations."""

from shapely.geometry import Point, Polygon

from citysense.geo.geometry import buffer_metres, centroid, make_valid_geometry


def test_centroid_point() -> None:
    """Test centroid of point."""
    p = Point(24.9, 60.1)
    c = centroid(p)
    assert c is not None
    assert c.x == 24.9
    assert c.y == 60.1


def test_centroid_polygon() -> None:
    """Test centroid of polygon."""
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    c = centroid(poly)
    assert c is not None
    assert c.x == 0.5
    assert c.y == 0.5


def test_centroid_empty() -> None:
    """Test centroid of empty geometry returns None."""
    from shapely.geometry import LineString

    empty = LineString()
    c = centroid(empty)
    assert c is None


def test_make_valid_geometry() -> None:
    """Test make_valid_geometry."""
    poly = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    out = make_valid_geometry(poly)
    assert out is not None
    assert out.is_valid


def test_buffer_metres_epsg4326() -> None:
    """Test buffer in WGS84."""
    p = Point(24.9, 60.1)
    buffered = buffer_metres(p, 100.0, crs_epsg=4326)
    assert buffered is not None
    assert buffered.area > 0


def test_buffer_metres_projected() -> None:
    """Test buffer in projected CRS."""
    p = Point(24.9, 60.1)
    buffered = buffer_metres(p, 100.0, crs_epsg=3067)
    assert buffered is not None
