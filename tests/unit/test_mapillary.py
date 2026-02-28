"""Unit tests for Mapillary connector with mocks."""

import pytest

from citysense.connectors.mapillary import MapillaryConnector
from citysense.geo.bbox import BBox


def test_mapillary_source_id() -> None:
    """Test MapillaryConnector source_id."""
    conn = MapillaryConnector(access_token="test")
    assert conn.source_id == "mapillary_v4"


def test_mapillary_license() -> None:
    """Test MapillaryConnector license."""
    conn = MapillaryConnector(access_token="test")
    assert "CC" in conn.license


def test_mapillary_rate_limit() -> None:
    """Test rate_limit_rps default."""
    conn = MapillaryConnector(access_token="test")
    assert conn.rate_limit_rps >= 0


@pytest.mark.asyncio
async def test_mapillary_fetch_mock() -> None:
    """Test Mapillary fetch with mocked HTTP."""
    from unittest.mock import AsyncMock, MagicMock, patch

    mock_response = MagicMock()
    mock_response.json.return_value = {"data": []}
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()

    with patch("citysense.connectors.mapillary.httpx.AsyncClient") as m:
        client = m.return_value.__aenter__.return_value
        client.get = AsyncMock(return_value=mock_response)
        conn = MapillaryConnector(access_token="valid_token")
        bbox = BBox(west=24.9, south=60.1, east=24.92, north=60.12)
        gdf = await conn.fetch(bbox)
        assert "geometry" in gdf.columns or len(gdf) == 0
