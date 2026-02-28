"""Unit tests for service registry."""

from citysense.core.registry import get_registry, init


def test_init_default() -> None:
    """Test init with defaults."""
    reg = init()
    assert reg is not None
    assert reg.config is not None


def test_init_with_pilot() -> None:
    """Test init with pilot override."""
    reg = init(pilot="fi")
    assert reg.get("pilot_country") == "fi"


def test_registry_get_set() -> None:
    """Test registry get/set."""
    init()
    reg = get_registry()
    reg.set("test_key", "test_value")
    assert reg.get("test_key") == "test_value"
    assert reg.get("nonexistent", "default") == "default"


def test_registry_config() -> None:
    """Test registry config property."""
    reg = init()
    config = reg.config
    assert config.vector_store_url == "http://localhost:6333"
