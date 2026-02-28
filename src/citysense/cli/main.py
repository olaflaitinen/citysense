"""Typer 0.15.x root CLI.

CitySense command-line interface for pilot management, index building,
natural language queries, and MCP server.
"""

import asyncio
import os
from pathlib import Path

import typer

from citysense import __version__

app = typer.Typer(
    name="citysense",
    help="Geospatial RAG and MCP server for urban AI development; WUF13 aligned.",
)


@app.callback()
def main_callback(
    version: bool = typer.Option(False, "--version", "-v", help="Print version"),
) -> None:
    """CitySense CLI."""
    if version:
        typer.echo(f"citysense {__version__}")
        raise typer.Exit()


@app.command()
def pilot(
    action: str = typer.Argument(..., help="init | sync | status"),
    country: str | None = typer.Argument(None, help="Country code (az, fi, se, dk, no)"),
) -> None:
    """Manage pilot configuration."""
    valid = ("az", "fi", "se", "dk", "no")
    c = (country or "").lower()
    if action == "init":
        if c not in valid:
            typer.echo(f"Country must be one of: {', '.join(valid)}")
            raise typer.Exit(1)
        env_path = Path(".env")
        content = env_path.read_text() if env_path.exists() else ""
        if "CITYSENSE_PILOT_COUNTRY" not in content:
            env_path.parent.mkdir(parents=True, exist_ok=True)
            with env_path.open("a") as f:
                if content and not content.endswith("\n"):
                    f.write("\n")
                f.write(f"CITYSENSE_PILOT_COUNTRY={c}\n")
        typer.echo(f"Pilot initialised: {c}")
    elif action == "status":
        pc = os.environ.get("CITYSENSE_PILOT_COUNTRY", "not set")
        typer.echo(f"Pilot country: {pc}")
    else:
        typer.echo(f"Action {action} not implemented")


@app.command()
def index(
    action: str = typer.Argument(..., help="build | update | status"),
    city: str | None = typer.Option(None, "--city", "-c", help="City name"),
    sources: str | None = typer.Option(
        "osm", "--sources", "-s", help="Comma-separated: osm,mapillary,kartatview,sentinel"
    ),
    country: str | None = typer.Option("fi", "--country", help="ISO2 country code"),
) -> None:
    """Manage spatial index."""

    async def _run() -> None:
        from citysense.connectors.osm import OSMConnector
        from citysense.pilot.az import BAKU_BBOX
        from citysense.pilot.fi import HELSINKI_BBOX
        from citysense.rag.index.builder import build_index

        bbox_map = {"Helsinki": HELSINKI_BBOX, "Baku": BAKU_BBOX}
        bbox = bbox_map.get(city or "Helsinki", HELSINKI_BBOX)

        if action == "build":
            connector = OSMConnector()
            gdf = await connector.fetch(bbox, country=country or "fi")
            if gdf.empty:
                typer.echo("No features fetched")
                return
            n = await build_index(gdf, country=country or "fi")
            typer.echo(f"Indexed {n} chunks to cs_{country or 'fi'}_urban")
        elif action == "status":
            from qdrant_client import QdrantClient

            url = os.environ.get("CITYSENSE_VECTOR_STORE_URL", "http://localhost:6333")
            try:
                client = QdrantClient(url=url)
                coll = f"cs_{country or 'fi'}_urban"
                info = client.get_collection(coll)
                typer.echo(f"Collection {coll}: {info.points_count} points")
            except Exception as e:
                typer.echo(f"Status error: {e}")
        else:
            typer.echo(f"Action {action} not implemented")

    asyncio.run(_run())


@app.command()
def query(
    query_str: str = typer.Argument(..., help="Natural language query"),
    country: str | None = typer.Option(None, "--country", "-c"),
    city: str | None = typer.Option(None, "--city"),
) -> None:
    """Execute natural language spatial query."""

    async def _run() -> None:
        from citysense.rag.pipeline import run_pipeline

        result = await run_pipeline(
            query=query_str,
            country=country,
            city=city,
        )
        typer.echo(result.context_summary)

    asyncio.run(_run())


@app.command()
def serve(
    transport: str = typer.Option("stdio", "--transport", "-t", help="stdio | sse"),
    port: int = typer.Option(7832, "--port", "-p"),
) -> None:
    """Start MCP server."""
    if transport == "stdio":
        from citysense.mcp.server import app as mcp_app

        mcp_app.run(transport="stdio")
    else:
        typer.echo(f"SSE server on port {port}")


if __name__ == "__main__":
    app()
