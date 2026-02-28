"""Index construction from GeoDataFrame inputs."""

import hashlib
from datetime import UTC, datetime
from typing import Any

import geopandas as gpd
from qdrant_client.models import PointStruct

from citysense.geo.h3 import polyfill
from citysense.rag.embedder import embed_texts
from citysense.rag.index.store import ensure_collection, get_collection_name, upsert_chunks


def _chunk_text(row: gpd.GeoSeries, feature_type: str) -> str:
    """Generate natural language description for chunk."""
    props = row.get("properties", {}) or {}
    subtype = row.get("feature_subtype", "")
    name = props.get("name", row.get("name", ""))
    parts = [f"{feature_type} feature"]
    if subtype:
        parts.append(f"({subtype})")
    if name:
        parts.append(f"named {name}")
    return " ".join(parts)


def _chunk_id(source_id: str, feature_id: str) -> str:
    """Generate deterministic chunk ID from source and feature."""
    content = f"{source_id}:{feature_id}"
    return hashlib.sha256(content.encode()).hexdigest()[:32]


async def build_index(
    gdf: gpd.GeoDataFrame,
    country: str,
    qdrant_url: str = "http://localhost:6333",
    collection_prefix: str = "cs",
    embed_model: str = "BAAI/bge-m3",
) -> int:
    """Build Qdrant index from GeoDataFrame.

    Args:
        gdf: GeoDataFrame with normalised schema.
        country: ISO2 country code.
        qdrant_url: Qdrant server URL.
        collection_prefix: Collection name prefix.
        embed_model: Text embedding model.

    Returns:
        Number of points upserted.
    """
    from qdrant_client import QdrantClient

    collection = get_collection_name(collection_prefix, country)
    client = QdrantClient(url=qdrant_url)
    ensure_collection(client, collection)

    texts: list[str] = []
    rows_data: list[dict[str, Any]] = []
    for _, row in gdf.iterrows():
        geom = row.get("geometry")
        if geom is None or geom.is_empty:
            continue
        ft = row.get("feature_type", "unknown")
        text = _chunk_text(row, ft)
        texts.append(text)
        h3_cells = list(polyfill(geom, 9))
        geo_dict = None
        if hasattr(geom, "__geo_interface__"):
            geo_dict = geom.__geo_interface__
        rows_data.append(
            {
                "feature_id": row.get("feature_id", ""),
                "source_id": row.get("source_id", ""),
                "text": text,
                "geometry": geo_dict,
                "h3_cells": h3_cells,
                "properties": dict(row.get("properties", {}) or {}),
                "wuf13_tags": list(row.get("wuf13_tags", []) or []),
                "sdg_tags": list(row.get("sdg_tags", []) or []),
            }
        )

    if not texts:
        return 0

    vectors = embed_texts(texts, model=embed_model)
    points: list[PointStruct] = []
    for vec, data in zip(vectors, rows_data, strict=True):
        chunk_id = _chunk_id(data["source_id"], data["feature_id"])
        payload = {
            "chunk_id": chunk_id,
            "text": data["text"],
            "geometry": data["geometry"],
            "h3_cells": data["h3_cells"],
            "properties": data["properties"],
            "source_id": data["source_id"],
            "country": country,
            "wuf13_tags": data["wuf13_tags"],
            "sdg_tags": data["sdg_tags"],
            "embedded_at": datetime.now(UTC).isoformat(),
        }
        pt_id = int(hashlib.sha256(chunk_id.encode()).hexdigest()[:16], 16)
        points.append(PointStruct(id=pt_id, vector=vec, payload=payload))

    upsert_chunks(client, collection, points)
    return len(points)
