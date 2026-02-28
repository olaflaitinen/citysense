"""Unit tests for reranker."""

from citysense.rag.reranker import rerank


def test_rerank_fallback_no_encoder() -> None:
    """Test rerank returns top-k when TextCrossEncoder unavailable."""
    candidates = [
        {"text": "First", "id": 1},
        {"text": "Second", "id": 2},
        {"text": "Third", "id": 3},
    ]
    result = rerank("query", candidates, top_k=2)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


def test_rerank_custom_text_key() -> None:
    """Test rerank with custom text key."""
    candidates = [{"content": "A", "id": 1}, {"content": "B", "id": 2}]
    result = rerank("q", candidates, text_key="content", top_k=1)
    assert len(result) == 1


def test_rerank_empty_candidates() -> None:
    """Test rerank with empty list."""
    result = rerank("q", [], top_k=5)
    assert result == []
