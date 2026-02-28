"""Unit tests for CRS operations."""

import pytest

import geopandas as gpd
from shapely.geometry import Point

from citysense.geo.crs import get_national_crs, normalize


def test_get_national_crs() -> None:
    """Test national CRS lookup."""
    assert get_national_crs("fi") == "EPSG:3067"
    assert get_national_crs("az") == "EPSG:32638"
    assert get_national_crs("se") == "EPSG:3006"
    assert get_national_crs("dk") == "EPSG:25832"
    assert get_national_crs("no") == "EPSG:25833"
    assert get_national_crs("xx") == "EPSG:4326"
    assert get_national_crs("FI") == "EPSG:3067"


def test_normalize_same_crs() -> None:
    """Test normalize when already in target CRS."""
    gdf = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[Point(24.9, 60.1)],
        crs="EPSG:4326",
    )
    out = normalize(gdf, target="EPSG:4326")
    assert out.crs == gdf.crs


def test_normalize_no_crs() -> None:
    """Test normalize raises when GeoDataFrame has no CRS."""
    gdf = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[Point(24.9, 60.1)],
    )
    with pytest.raises(ValueError, match="no CRS"):
        normalize(gdf)


def test_normalize_reproject() -> None:
    """Test normalize reprojects to target."""
    gdf = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[Point(24.9, 60.1)],
        crs="EPSG:4326",
    )
    out = normalize(gdf, target="EPSG:3067")
    assert str(out.crs) == "EPSG:3067"
