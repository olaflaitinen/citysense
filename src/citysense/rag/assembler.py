"""Context assembly and SpatialChunk serialisation."""

from dataclasses import dataclass
from typing import Any


@dataclass
class SpatialChunk:
    """Retrieved spatial chunk schema (Qdrant payload).

    Attributes:
        chunk_id: sha256 of (source_id, feature_id, embedded_at).
        text: Template-generated natural language description.
        geometry: GeoJSON geometry dict.
        h3_cells: H3 resolution 9 cell set.
        properties: Pass-through feature properties.
        source_id: Connector identifier.
        country: ISO2.
        wuf13_tags: WUF13 dimension labels.
        sdg_tags: SDG indicator codes.
        embedded_at: ISO 8601 UTC.
        street_condition_score: Optional from imagery fusion.
        ndvi: Optional Sentinel-2 NDVI.
        ndbi: Optional Sentinel-2 NDBI.
        sar_vv_mean_db: Optional Sentinel-1 VV backscatter.
    """

    chunk_id: str
    text: str
    geometry: dict[str, Any]
    h3_cells: list[str]
    properties: dict[str, Any]
    source_id: str
    country: str
    wuf13_tags: list[str]
    sdg_tags: list[str]
    embedded_at: str
    street_condition_score: float | None = None
    ndvi: float | None = None
    ndbi: float | None = None
    sar_vv_mean_db: float | None = None


def assemble_context(
    chunks: list[dict[str, Any]],
    max_chars: int = 4000,
) -> tuple[list[dict[str, Any]], str]:
    """Assemble retrieved chunks into context and summary.

    Args:
        chunks: List of chunk payloads.
        max_chars: Max context length in characters.

    Returns:
        (chunks, context_summary) tuple.
    """
    total = 0
    selected: list[dict[str, Any]] = []
    for c in chunks:
        text = c.get("text", "")
        if total + len(text) > max_chars:
            break
        selected.append(c)
        total += len(text)
    summary = f"Retrieved {len(selected)} spatial chunks. "
    if selected:
        summary += "Primary sources: " + ", ".join(
            {str(c.get("source_id", "unknown")) for c in selected[:5]}
        )
    return selected, summary
