"""Main RAG orchestration: 7-step pipeline."""

from dataclasses import dataclass, field
from typing import Any

from citysense.geo.h3 import bbox_to_h3_set
from citysense.rag.assembler import assemble_context
from citysense.rag.embedder import embed_texts
from citysense.rag.intent import parse_intent
from citysense.rag.reranker import rerank
from citysense.rag.retriever import hybrid_search


@dataclass
class CitySenseResult:
    """RAG pipeline result envelope."""

    query: str
    country: str | None = None
    city: str | None = None
    results: list[dict[str, Any]] = field(default_factory=list)
    context_summary: str = ""
    pipeline_steps_ms: dict[str, int] = field(default_factory=dict)
    data_sources: list[str] = field(default_factory=list)
    wuf13_alignment: list[str] = field(default_factory=list)
    sdg_indicators: list[str] = field(default_factory=list)


async def run_pipeline(
    query: str,
    country: str | None = None,
    city: str | None = None,
    max_results: int = 5,
    qdrant_url: str = "http://localhost:6333",
    collection_prefix: str = "cs",
) -> CitySenseResult:
    """Execute the 7-step RAG pipeline.

    Step 1: Intent parsing
    Step 2: Spatial pre-filter (H3 cells)
    Step 3: Dense vector search
    Step 4: Sparse BM25 search
    Step 5: RRF merge
    Step 6: Cross-encoder rerank
    Step 7: Context assembly

    Args:
        query: Natural language query.
        country: Override country scope.
        city: Override city scope.
        max_results: Max chunks to return.
        qdrant_url: Qdrant server URL.
        collection_prefix: Collection name prefix.

    Returns:
        CitySenseResult with chunks and metadata.
    """
    import time

    from qdrant_client import QdrantClient

    steps: dict[str, int] = {}
    t0 = time.perf_counter()

    intent = parse_intent(query)
    steps["intent_parse"] = int((time.perf_counter() - t0) * 1000)

    country = country or intent.country_scope or "fi"
    collection = f"{collection_prefix}_{country}_urban"

    h3_cells: list[str] | None = None
    if intent.bbox:
        h3_cells = list(bbox_to_h3_set(intent.bbox, 9))
    steps["spatial_prefilter"] = int((time.perf_counter() - t0) * 1000)

    vectors = embed_texts([query])
    query_vector = vectors[0]
    steps["embed"] = int((time.perf_counter() - t0) * 1000)

    client = QdrantClient(url=qdrant_url)
    try:
        candidates = hybrid_search(
            client=client,
            collection=collection,
            query_vector=query_vector,
            query_text=query,
            h3_filter=h3_cells,
            limit=20,
        )
    except Exception:
        candidates = []
    steps["hybrid_search"] = int((time.perf_counter() - t0) * 1000)

    reranked = rerank(query, candidates, top_k=max_results)
    steps["rerank"] = int((time.perf_counter() - t0) * 1000)

    chunks, summary = assemble_context([c.get("payload", c) for c in reranked])
    steps["assemble"] = int((time.perf_counter() - t0) * 1000)

    sources = list({c.get("source_id", "") for c in chunks if c.get("source_id")})
    wuf13 = []
    for c in chunks:
        wuf13.extend(c.get("wuf13_tags", []))
    sdg = []
    for c in chunks:
        sdg.extend(c.get("sdg_tags", []))

    return CitySenseResult(
        query=query,
        country=country,
        city=city or intent.city_scope,
        results=chunks,
        context_summary=summary,
        pipeline_steps_ms=steps,
        data_sources=sources,
        wuf13_alignment=list(dict.fromkeys(wuf13)),
        sdg_indicators=list(dict.fromkeys(sdg)),
    )
