"""Abstract BaseConnector interface."""

from abc import ABC, abstractmethod
from typing import Any

import geopandas as gpd

from citysense.geo.bbox import BBox


class BaseConnector(ABC):
    """Abstract base for all data connectors."""

    @abstractmethod
    async def fetch(self, bbox: BBox, **kwargs: Any) -> gpd.GeoDataFrame:
        """Fetch data for bounding box.

        Args:
            bbox: Bounding box in EPSG:4326.
            **kwargs: Connector-specific parameters.

        Returns:
            GeoDataFrame with normalised schema.
        """
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Check connector availability.

        Returns:
            True if connector is operational.
        """
        ...

    @property
    @abstractmethod
    def source_id(self) -> str:
        """Connector identifier for indexing."""
        ...

    @property
    @abstractmethod
    def license(self) -> str:
        """Data source license."""
        ...

    @property
    def rate_limit_rps(self) -> float:
        """Requests per second limit. Default 1.0."""
        return 1.0
