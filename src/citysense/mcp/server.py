"""FastMCP server entry point (mcp 1.4.x)."""

from typing import Any, Literal

from mcp.server.fastmcp import FastMCP

from citysense.mcp.tools.spatial_query import query_spatial_context_impl

app = FastMCP(
    name="citysense",
    instructions="Urban geospatial intelligence server; WUF13 and SDG 11 aligned.",
)


@app.tool()
async def query_spatial_context(
    query: str,
    country: str | None = None,
    city: str | None = None,
    max_results: int = 5,
    output_format: Literal["geojson", "summary", "both"] = "summary",
) -> dict[str, Any]:
    """Query spatial context using natural language."""
    return await query_spatial_context_impl(
        query=query,
        country=country,
        city=city,
        max_results=max_results,
        output_format=output_format,
    )
