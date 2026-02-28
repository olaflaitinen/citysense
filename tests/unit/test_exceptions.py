"""Unit tests for exception hierarchy."""

import pytest

from citysense.core.exceptions import (
    BBoxTooLargeError,
    CDSEAuthError,
    CitySenseError,
    ConnectorAuthError,
    ConnectorRateLimitError,
    CRSMismatchError,
    DataNotAvailableError,
    DataSourceError,
    EmbeddingError,
    ImageryError,
    IndexNotBuiltError,
    InvalidGeometryError,
    MapillaryQuotaError,
    MCPError,
    PilotConfigError,
    ResourceNotFoundError,
    RetrievalError,
    RAGError,
    SentinelTileUnavailableError,
    SpatialError,
    ToolExecutionError,
)


def test_citysense_error_base() -> None:
    """Test CitySenseError is base."""
    err = CitySenseError("test")
    assert str(err) == "test"


def test_data_source_errors() -> None:
    """Test DataSourceError hierarchy."""
    assert issubclass(ConnectorAuthError, DataSourceError)
    assert issubclass(ConnectorRateLimitError, DataSourceError)
    assert issubclass(DataNotAvailableError, DataSourceError)
    err = ConnectorAuthError("invalid token")
    assert "invalid token" in str(err)


def test_spatial_errors() -> None:
    """Test SpatialError hierarchy."""
    assert issubclass(CRSMismatchError, SpatialError)
    assert issubclass(InvalidGeometryError, SpatialError)
    assert issubclass(BBoxTooLargeError, SpatialError)
    err = BBoxTooLargeError("bbox too large")
    assert "bbox too large" in str(err)


def test_rag_errors() -> None:
    """Test RAGError hierarchy."""
    assert issubclass(IndexNotBuiltError, RAGError)
    assert issubclass(EmbeddingError, RAGError)
    assert issubclass(RetrievalError, RAGError)


def test_imagery_errors() -> None:
    """Test ImageryError hierarchy."""
    assert issubclass(MapillaryQuotaError, ImageryError)
    assert issubclass(CDSEAuthError, ImageryError)
    assert issubclass(SentinelTileUnavailableError, ImageryError)


def test_mcp_errors() -> None:
    """Test MCPError hierarchy."""
    assert issubclass(ToolExecutionError, MCPError)
    assert issubclass(ResourceNotFoundError, MCPError)


def test_pilot_config_error() -> None:
    """Test PilotConfigError."""
    err = PilotConfigError("missing country")
    assert issubclass(PilotConfigError, CitySenseError)
    assert "missing country" in str(err)
