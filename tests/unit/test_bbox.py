"""Unit tests for BBox."""

import pytest

from citysense.geo.bbox import BBox


def test_bbox_creation() -> None:
    """Test BBox creation and validation."""
    b = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
    assert b.west == 24.9
    assert b.south == 60.1
    assert b.east == 25.0
    assert b.north == 60.2


def test_bbox_invalid_west_east() -> None:
    """Test invalid west >= east raises."""
    with pytest.raises(ValueError, match="west must be less than east"):
        BBox(west=25.0, south=60.1, east=24.9, north=60.2)


def test_bbox_invalid_south_north() -> None:
    """Test invalid south >= north raises."""
    with pytest.raises(ValueError, match="south must be less than north"):
        BBox(west=24.9, south=60.2, east=25.0, north=60.1)


def test_bbox_intersection() -> None:
    """Test bbox intersection."""
    a = BBox(west=24.9, south=60.1, east=25.1, north=60.3)
    b = BBox(west=25.0, south=60.15, east=25.2, north=60.25)
    inter = a.intersection(b)
    assert inter is not None
    assert inter.west == 25.0
    assert inter.south == 60.15
    assert inter.east == 25.1
    assert inter.north == 60.25


def test_bbox_intersection_disjoint() -> None:
    """Test bbox intersection returns None when disjoint."""
    a = BBox(west=24.0, south=60.0, east=24.5, north=60.5)
    b = BBox(west=25.0, south=61.0, east=25.5, north=61.5)
    assert a.intersection(b) is None


def test_bbox_to_tuple() -> None:
    """Test to_tuple."""
    b = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
    assert b.to_tuple() == (24.9, 60.1, 25.0, 60.2)


def test_bbox_area_km2() -> None:
    """Test area_km2 property."""
    b = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
    area = b.area_km2
    assert area > 0
    assert area < 100


def test_bbox_expand() -> None:
    """Test expand by factor."""
    b = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
    expanded = b.expand(2.0)
    assert expanded.west < b.west
    assert expanded.east > b.east
    assert expanded.south < b.south
    assert expanded.north > b.north
