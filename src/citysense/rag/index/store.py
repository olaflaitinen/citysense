"""Qdrant collection management and upsert."""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


def get_collection_name(prefix: str, country: str) -> str:
    """Get collection name for country."""
    return f"{prefix}_{country}_urban"


def ensure_collection(
    client: QdrantClient,
    collection: str,
    vector_size: int = 1024,
) -> None:
    """Create collection if not exists."""
    collections = client.get_collections().collections
    names = [c.name for c in collections]
    if collection not in names:
        client.create_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )


def upsert_chunks(
    client: QdrantClient,
    collection: str,
    points: list[PointStruct],
) -> None:
    """Upsert points to collection."""
    if points:
        client.upsert(collection_name=collection, points=points)
