"""Overpass QL query builder with async batching."""

from typing import Any, cast

import httpx

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


async def overpass_query(
    query: str,
    timeout: float = 180.0,
    url: str = OVERPASS_URL,
) -> dict[str, Any]:
    """Execute Overpass API query.

    Args:
        query: Overpass QL query string.
        timeout: Request timeout in seconds.
        url: Overpass API endpoint.

    Returns:
        JSON response with elements.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            data={"data": query},
            timeout=timeout,
        )
        response.raise_for_status()
        return cast(dict[str, Any], response.json())


def build_bbox_query(
    bbox: tuple[float, float, float, float],
    tags: list[tuple[str, str]],
    out_format: str = "json",
) -> str:
    """Build Overpass QL query for bbox and tags.

    Args:
        bbox: (west, south, east, north) in degrees.
        tags: List of (key, value) OSM tag filters.
        out_format: Output format (json, xml).

    Returns:
        Overpass QL query string.
    """
    west, south, east, north = bbox
    bbox_str = f"{south},{west},{north},{east}"
    tag_filters = "".join(f'["{k}"="{v}"]' if v else f'["{k}"]' for k, v in tags)
    return f"""
    [out:{out_format}][timeout:90];
    (
      node{tag_filters}({bbox_str});
      way{tag_filters}({bbox_str});
      relation{tag_filters}({bbox_str});
    );
    out body;
    >;
    out skel qt;
    """
