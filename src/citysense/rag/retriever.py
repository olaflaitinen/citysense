"""Hybrid retriever: Qdrant dense + BM25 sparse, RRF merge."""

from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

RRF_K = 60


def rrf_merge(
    dense_results: list[tuple[str, float]],
    sparse_results: list[tuple[str, float]],
    k: int = RRF_K,
) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion merge.

    $$\\text{RRF}(d) = \\sum_{R \\in \\{R_{\\text{dense}}, R_{\\text{sparse}}\\}}
    \\frac{1}{k + \\text{rank}_R(d)}$$

    Args:
        dense_results: [(id, score), ...] from dense search.
        sparse_results: [(id, score), ...] from BM25.
        k: Smoothing constant (default 60).

    Returns:
        Merged list of (id, rrf_score) sorted by score descending.
    """
    scores: dict[str, float] = {}
    for rank, (doc_id, _) in enumerate(dense_results, start=1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    for rank, (doc_id, _) in enumerate(sparse_results, start=1):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)
    return sorted(scores.items(), key=lambda x: -x[1])


def hybrid_search(
    client: QdrantClient,
    collection: str,
    query_vector: list[float],
    query_text: str,
    h3_filter: list[str] | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Execute hybrid search (dense primary; sparse fallback) with optional H3 filter.

    Args:
        client: Qdrant client.
        collection: Collection name.
        query_vector: Dense embedding vector.
        query_text: Raw query (for future BM25).
        h3_filter: Optional H3 cell filter.
        limit: Max results.

    Returns:
        List of result payloads.
    """
    q_filter = None
    if h3_filter:
        q_filter = Filter(
            should=[
                FieldCondition(key="h3_cells", match=MatchValue(value=h)) for h in h3_filter[:50]
            ]
        )
    try:
        dense = client.query_points(
            collection_name=collection,
            query=query_vector,
            limit=limit,
            query_filter=q_filter,
        )
    except Exception:
        return []
    results = []
    for p in dense.points:
        payload = p.payload or {}
        payload["_id"] = str(p.id)
        payload["_score"] = p.score
        results.append({"id": str(p.id), "payload": payload})
    return results
