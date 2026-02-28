"""Service locator for singletons."""

from typing import Any, TypeVar

from citysense.core.config import CitySenseConfig

T = TypeVar("T")

_registry: dict[str, Any] = {}
_config: CitySenseConfig | None = None


def init(
    pilot: str | None = None,
    config: CitySenseConfig | None = None,
) -> "CitySenseRegistry":
    """Initialise CitySense and populate the service registry.

    Args:
        pilot: Pilot country code (az, fi, se, dk, no). Overrides config.
        config: Optional config instance. If None, loads from env/toml.

    Returns:
        Registry instance for service access.
    """
    global _config, _registry
    _config = config or CitySenseConfig()
    if pilot:
        _registry["pilot_country"] = pilot
    else:
        _registry["pilot_country"] = _config.pilot_country
    return get_registry()


def get_registry() -> "CitySenseRegistry":
    """Get the global registry instance.

    Returns:
        CitySenseRegistry for service lookup.
    """
    return CitySenseRegistry()


class CitySenseRegistry:
    """Service locator for CitySense singletons."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get a registered service by key.

        Args:
            key: Service identifier.
            default: Default value if key not found.

        Returns:
            Registered service or default.
        """
        return _registry.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Register a service.

        Args:
            key: Service identifier.
            value: Service instance.
        """
        _registry[key] = value

    @property
    def config(self) -> CitySenseConfig:
        """Get the current configuration."""
        if _config is None:
            return CitySenseConfig()
        return _config
