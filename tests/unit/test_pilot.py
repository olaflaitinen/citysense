"""Unit tests for pilot configurations."""

from citysense.geo.bbox import BBox
from citysense.pilot.base import PilotConfig
from citysense.pilot.fi import FI_CONFIG, HELSINKI_BBOX


def test_pilot_config() -> None:
    """Test PilotConfig structure."""
    config = PilotConfig(
        country="fi",
        language="fi",
        national_crs="EPSG:3067",
        default_cities={"Helsinki": BBox(west=24.8, south=60.1, east=25.3, north=60.35)},
        connector_priority=("osm",),
        wuf13_primary_dimensions=("resilience",),
        data_gaps={},
        informality_heuristic=False,
    )
    assert config.country == "fi"
    assert config.national_crs == "EPSG:3067"
    assert "Helsinki" in config.default_cities


def test_fi_config() -> None:
    """Test Finland pilot config."""
    assert FI_CONFIG.country == "fi"
    assert "Helsinki" in FI_CONFIG.default_cities
    assert "osm" in FI_CONFIG.connector_priority


def test_helsinki_bbox() -> None:
    """Test Helsinki bbox bounds."""
    assert HELSINKI_BBOX.west == 24.80
    assert HELSINKI_BBOX.south == 60.10
    assert HELSINKI_BBOX.east == 25.30
    assert HELSINKI_BBOX.north == 60.35
