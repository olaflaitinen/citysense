"""Cross-encoder reranking via fastembed TextCrossEncoder."""

from typing import Any

try:
    from fastembed import TextCrossEncoder
except ImportError:
    TextCrossEncoder = None


def rerank(
    query: str,
    candidates: list[dict[str, Any]],
    text_key: str = "text",
    top_k: int = 5,
    model: str = "Xenova/ms-marco-MiniLM-L-6-v2",
) -> list[dict[str, Any]]:
    """Rerank candidates with cross-encoder.

    $$s_i = \\text{CrossEncoder}(q, c_i)$$

    Args:
        query: Query string.
        candidates: List of candidate dicts with text_key.
        text_key: Key for candidate text.
        top_k: Number of results to return.
        model: Cross-encoder model.

    Returns:
        Top-k candidates with scores.
    """
    if TextCrossEncoder is None:
        return candidates[:top_k]
    encoder = TextCrossEncoder(model_name=model)
    pairs = [(query, c.get(text_key, "")) for c in candidates]
    scores = list(encoder.rank(pairs))
    scored = list(zip(candidates, scores, strict=False))
    scored.sort(key=lambda x: -x[1])
    return [c for c, _ in scored[:top_k]]
