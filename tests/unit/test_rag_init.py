"""Unit tests for RAG module __getattr__."""

import pytest

from citysense.rag import SpatialIntent, assemble_context, parse_intent


def test_rag_exports() -> None:
    """Test direct RAG exports."""
    assert SpatialIntent is not None
    assert parse_intent is not None
    assert assemble_context is not None


def test_rag_getattr_invalid() -> None:
    """Test __getattr__ raises for invalid name."""
    import citysense.rag as rag

    with pytest.raises(AttributeError, match="has no attribute"):
        _ = rag.InvalidName
