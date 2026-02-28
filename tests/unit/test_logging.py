"""Unit tests for structured logging."""

from citysense.core.logging import bind_context, configure_logging, get_logger


def test_configure_logging() -> None:
    """Test logging configuration."""
    configure_logging(level="INFO")


def test_get_logger() -> None:
    """Test logger retrieval."""
    logger = get_logger("citysense.test")
    assert logger is not None


def test_bind_context() -> None:
    """Test context binding."""
    bind_context(request_id="test-123")
