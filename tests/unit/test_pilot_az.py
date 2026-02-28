"""Unit tests for Azerbaijan pilot."""

from citysense.pilot.az import AZ_CONFIG, BAKU_BBOX


def test_baku_bbox() -> None:
    """Test Baku bbox bounds."""
    assert BAKU_BBOX.west == 49.70
    assert BAKU_BBOX.south == 40.30
    assert BAKU_BBOX.east == 50.10
    assert BAKU_BBOX.north == 40.55


def test_az_config() -> None:
    """Test Azerbaijan pilot config."""
    assert AZ_CONFIG.country == "az"
    assert "Baku" in AZ_CONFIG.default_cities
    assert AZ_CONFIG.informality_heuristic is True
