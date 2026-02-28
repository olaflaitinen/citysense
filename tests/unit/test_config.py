"""Unit tests for CitySenseConfig."""

import pytest

from citysense.core.config import CitySenseConfig


def test_config_defaults() -> None:
    """Test default configuration values."""
    config = CitySenseConfig()
    assert config.pilot_country is None
    assert config.log_level == "INFO"
    assert config.vector_store_url == "http://localhost:6333"
    assert config.embedding_model == "BAAI/bge-m3"
    assert config.default_crs == "EPSG:4326"
    assert config.h3_resolution_fine == 9
    assert config.mcp_transport == "stdio"


def test_config_frozen() -> None:
    """Test config is immutable."""
    config = CitySenseConfig()
    with pytest.raises((ValueError, AttributeError)):
        config.log_level = "DEBUG"


def test_config_pilot_country_literal() -> None:
    """Test pilot_country accepts valid literals."""
    config = CitySenseConfig(pilot_country="fi")
    assert config.pilot_country == "fi"
