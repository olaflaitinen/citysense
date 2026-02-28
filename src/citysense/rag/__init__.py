"""Geospatial RAG pipeline: intent, retrieval, rerank, assembly."""

from citysense.rag.assembler import assemble_context
from citysense.rag.intent import SpatialIntent, parse_intent

__all__ = [
    "SpatialIntent",
    "parse_intent",
    "assemble_context",
]


def __getattr__(name: str) -> object:
    if name == "CitySenseResult":
        from citysense.rag.pipeline import CitySenseResult

        return CitySenseResult
    if name == "run_pipeline":
        from citysense.rag.pipeline import run_pipeline

        return run_pipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
