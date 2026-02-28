"""Text embedding via BAAI/bge-m3 (fastembed 0.4.2)."""

from fastembed import TextEmbedding


def get_embedder(model: str = "BAAI/bge-m3") -> TextEmbedding:
    """Get text embedder instance.

    Args:
        model: Model identifier for fastembed.

    Returns:
        TextEmbedding instance.
    """
    return TextEmbedding(model_name=model)


def embed_texts(texts: list[str], model: str = "BAAI/bge-m3") -> list[list[float]]:
    """Embed text strings.

    Args:
        texts: List of text strings.
        model: Embedding model identifier.

    Returns:
        List of embedding vectors (1024-dim for bge-m3).
    """
    embedder = get_embedder(model)
    return list(embedder.embed(texts))
