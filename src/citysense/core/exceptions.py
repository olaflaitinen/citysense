"""Exception hierarchy for CitySense.

Exception tree:
    CitySenseError (base)
    +-- DataSourceError
    |   +-- ConnectorAuthError
    |   +-- ConnectorRateLimitError
    |   +-- DataNotAvailableError
    +-- SpatialError
    |   +-- CRSMismatchError
    |   +-- InvalidGeometryError
    |   +-- BBoxTooLargeError
    +-- RAGError
    |   +-- IndexNotBuiltError
    |   +-- EmbeddingError
    |   +-- RetrievalError
    +-- ImageryError
    |   +-- MapillaryQuotaError
    |   +-- CDSEAuthError
    |   +-- SentinelTileUnavailableError
    +-- MCPError
    |   +-- ToolExecutionError
    |   +-- ResourceNotFoundError
    +-- PilotConfigError
"""


class CitySenseError(Exception):
    """Base exception for all CitySense errors."""


class DataSourceError(CitySenseError):
    """Error during data source access or connector operation."""


class ConnectorAuthError(DataSourceError):
    """Authentication failure with external data source."""


class ConnectorRateLimitError(DataSourceError):
    """Rate limit exceeded for external API."""


class DataNotAvailableError(DataSourceError):
    """Requested data not available for the given parameters."""


class SpatialError(CitySenseError):
    """Error in spatial operations or geometry handling."""


class CRSMismatchError(SpatialError):
    """Coordinate reference system mismatch or invalid transformation."""


class InvalidGeometryError(SpatialError):
    """Invalid or malformed geometry."""


class BBoxTooLargeError(SpatialError):
    """Bounding box exceeds allowed size limit."""


class RAGError(CitySenseError):
    """Error in RAG pipeline or retrieval operations."""


class IndexNotBuiltError(RAGError):
    """Index has not been built or is unavailable."""


class EmbeddingError(RAGError):
    """Error during text or image embedding."""


class RetrievalError(RAGError):
    """Error during vector or hybrid retrieval."""


class ImageryError(CitySenseError):
    """Error in imagery processing or access."""


class MapillaryQuotaError(ImageryError):
    """Mapillary API quota exceeded."""


class CDSEAuthError(ImageryError):
    """Copernicus Data Space Ecosystem authentication failure."""


class SentinelTileUnavailableError(ImageryError):
    """Sentinel tile not available for the requested parameters."""


class MCPError(CitySenseError):
    """Error in MCP server or tool execution."""


class ToolExecutionError(MCPError):
    """MCP tool execution failed."""


class ResourceNotFoundError(MCPError):
    """MCP resource not found."""


class PilotConfigError(CitySenseError):
    """Invalid or missing pilot configuration."""
