"""Unit tests for connectors."""

import pytest

from citysense.connectors import KartaViewConnector, MapillaryConnector, OSMConnector
from citysense.geo.bbox import BBox


def test_connectors_import() -> None:
    """Test connector exports."""
    from citysense.connectors import MapillaryConnector, OSMConnector

    assert MapillaryConnector is not None
    assert OSMConnector is not None


def test_mapillary_connector_properties() -> None:
    """Test MapillaryConnector properties."""
    conn = MapillaryConnector(access_token="test")
    assert conn.source_id == "mapillary_v4"
    assert "CC" in conn.license


def test_mapillary_connector_no_token() -> None:
    """Test MapillaryConnector raises without token."""
    from citysense.core.exceptions import ConnectorAuthError

    conn = MapillaryConnector(access_token=None)
    with pytest.raises(ConnectorAuthError):
        conn._check_token()


def test_kartaview_connector_properties() -> None:
    """Test KartaViewConnector properties."""
    conn = KartaViewConnector()
    assert "karta" in conn.source_id.lower()
    assert "CC" in conn.license


def test_osm_connector_properties() -> None:
    """Test OSMConnector properties."""
    conn = OSMConnector()
    assert conn.source_id == "osm"
    assert "ODbL" in conn.license or "Open" in conn.license


def test_osm_build_bbox_query() -> None:
    """Test OSM build_bbox_query."""
    from citysense.connectors.osm import build_bbox_query

    bbox = (24.9, 60.1, 25.0, 60.2)
    tags = [("amenity", "restaurant")]
    q = build_bbox_query(bbox, tags)
    assert "restaurant" in q


@pytest.mark.asyncio
async def test_kartaview_fetch_mock() -> None:
    """Test KartaView fetch with mocked HTTP."""
    from unittest.mock import AsyncMock, MagicMock, patch

    mock_response = MagicMock()
    mock_response.json.return_value = {"result": {"photos": [], "data": []}}
    mock_response.raise_for_status = MagicMock()

    with patch("citysense.connectors.kartaview.httpx.AsyncClient") as m:
        client = m.return_value.__aenter__.return_value
        client.get = AsyncMock(return_value=mock_response)
        conn = KartaViewConnector()
        bbox = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
        gdf = await conn.fetch(bbox)
        assert "geometry" in gdf.columns or len(gdf) == 0
