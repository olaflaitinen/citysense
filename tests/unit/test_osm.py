"""Unit tests for OSM Overpass query builder."""

import pytest

from citysense.geo.osm import build_bbox_query, overpass_query


def test_build_bbox_query() -> None:
    """Test Overpass QL query builder."""
    bbox = (24.9, 60.1, 25.0, 60.2)
    tags = [("amenity", "restaurant"), ("building", "")]
    q = build_bbox_query(bbox, tags)
    assert "24.9" in q or "60.1" in q
    assert "restaurant" in q
    assert "building" in q
    assert "[out:json]" in q or "[out:json]" in q.replace(" ", "")


def test_build_bbox_query_tag_only() -> None:
    """Test tag filter without value."""
    bbox = (0, 0, 1, 1)
    tags = [("highway", "")]
    q = build_bbox_query(bbox, tags)
    assert "highway" in q


@pytest.mark.asyncio
async def test_overpass_query_mock() -> None:
    """Test overpass_query with mocked HTTP."""
    from unittest.mock import AsyncMock, MagicMock, patch

    mock_response = MagicMock()
    mock_response.json.return_value = {"elements": []}
    mock_response.raise_for_status = MagicMock()

    with patch("citysense.geo.osm.httpx.AsyncClient") as mock_client:
        client_instance = AsyncMock()
        client_instance.post = AsyncMock(return_value=mock_response)
        mock_client.return_value.__aenter__ = AsyncMock(return_value=client_instance)
        mock_client.return_value.__aexit__ = AsyncMock(return_value=None)
        result = await overpass_query("[out:json];node(0,0,1,1);out;")
        assert "elements" in result
