"""query_spatial_context MCP tool implementation."""

from typing import Any, Literal

from citysense.rag.pipeline import run_pipeline


async def query_spatial_context_impl(
    query: str,
    country: str | None = None,
    city: str | None = None,
    max_results: int = 5,
    output_format: Literal["geojson", "summary", "both"] = "summary",
) -> dict[str, Any]:
    """Query spatial context using natural language.

    Args:
        query: Natural language spatial query.
        country: ISO2 country code.
        city: City name.
        max_results: Max chunks.
        output_format: Output format.

    Returns:
        CitySenseResult as dict.
    """
    result = await run_pipeline(
        query=query,
        country=country,
        city=city,
        max_results=max_results,
    )
    return {
        "citysense_version": "0.2.1",
        "query": result.query,
        "country": result.country,
        "city": result.city,
        "results": result.results,
        "context_summary": result.context_summary,
        "pipeline_steps_ms": result.pipeline_steps_ms,
        "data_sources": result.data_sources,
        "wuf13_alignment": result.wuf13_alignment,
        "sdg_indicators": result.sdg_indicators,
    }
