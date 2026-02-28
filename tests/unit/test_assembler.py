"""Unit tests for context assembler."""

from citysense.rag.assembler import SpatialChunk, assemble_context


def test_spatial_chunk() -> None:
    """Test SpatialChunk dataclass."""
    chunk = SpatialChunk(
        chunk_id="abc",
        text="Test feature",
        geometry={"type": "Point", "coordinates": [24.9, 60.1]},
        h3_cells=["891f1d48b7fffff"],
        properties={},
        source_id="osm",
        country="fi",
        wuf13_tags=[],
        sdg_tags=[],
        embedded_at="2025-01-01T00:00:00Z",
    )
    assert chunk.chunk_id == "abc"
    assert chunk.text == "Test feature"
    assert chunk.source_id == "osm"
    assert chunk.ndvi is None


def test_assemble_context_empty() -> None:
    """Test assemble_context with empty chunks."""
    selected, summary = assemble_context([], max_chars=100)
    assert selected == []
    assert "Retrieved 0" in summary


def test_assemble_context_single() -> None:
    """Test assemble_context with single chunk."""
    chunks = [{"text": "Short", "source_id": "osm"}]
    selected, summary = assemble_context(chunks, max_chars=1000)
    assert len(selected) == 1
    assert "Retrieved 1" in summary
    assert "osm" in summary


def test_assemble_context_truncate() -> None:
    """Test assemble_context truncates by max_chars."""
    chunks = [
        {"text": "A" * 100, "source_id": "a"},
        {"text": "B" * 100, "source_id": "b"},
        {"text": "C" * 100, "source_id": "c"},
    ]
    selected, _ = assemble_context(chunks, max_chars=150)
    assert len(selected) <= 2


def test_assemble_context_no_text_key() -> None:
    """Test assemble_context with missing text key."""
    chunks = [{"source_id": "x"}]
    selected, _ = assemble_context(chunks)
    assert len(selected) == 1
    assert selected[0].get("text", "") == ""
