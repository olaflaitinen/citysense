"""Unit tests for OSM connector (direct import to avoid sentinel)."""

import pytest

from citysense.connectors.osm import OSMConnector
from citysense.geo.bbox import BBox


def test_osm_connector_properties() -> None:
    """Test OSMConnector properties."""
    conn = OSMConnector()
    assert conn.source_id == "osm"
    assert "ODbL" in conn.license


@pytest.mark.asyncio
async def test_osm_fetch_mock() -> None:
    """Test OSM fetch with mocked overpass."""
    from unittest.mock import AsyncMock, patch

    mock_data = {
        "elements": [
            {"type": "node", "id": 1, "lon": 24.95, "lat": 60.15, "tags": {"amenity": "cafe"}},
        ]
    }
    with patch("citysense.connectors.osm.overpass_query", new_callable=AsyncMock) as m:
        m.return_value = mock_data
        conn = OSMConnector()
        bbox = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
        gdf = await conn.fetch(bbox)
        assert len(gdf) == 1
        assert "geometry" in gdf.columns


@pytest.mark.asyncio
async def test_osm_fetch_empty() -> None:
    """Test OSM fetch with empty response."""
    from unittest.mock import AsyncMock, patch

    with patch("citysense.connectors.osm.overpass_query", new_callable=AsyncMock) as m:
        m.return_value = {"elements": []}
        conn = OSMConnector()
        bbox = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
        gdf = await conn.fetch(bbox)
        assert len(gdf) == 0


@pytest.mark.asyncio
async def test_osm_fetch_way_with_geometry() -> None:
    """Test OSM fetch with way element."""
    from unittest.mock import AsyncMock, patch

    mock_data = {
        "elements": [
            {
                "type": "way",
                "id": 1,
                "geometry": [
                    {"lon": 24.9, "lat": 60.1},
                    {"lon": 25.0, "lat": 60.1},
                    {"lon": 25.0, "lat": 60.2},
                    {"lon": 24.9, "lat": 60.2},
                ],
                "tags": {"building": "yes"},
            },
        ]
    }
    with patch("citysense.connectors.osm.overpass_query", new_callable=AsyncMock) as m:
        m.return_value = mock_data
        conn = OSMConnector()
        bbox = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
        gdf = await conn.fetch(bbox)
        assert len(gdf) == 1
        assert gdf.iloc[0]["feature_type"] == "building"


@pytest.mark.asyncio
async def test_osm_health_check() -> None:
    """Test OSM health_check."""
    from unittest.mock import AsyncMock, patch

    with patch("citysense.connectors.osm.overpass_query", new_callable=AsyncMock) as m:
        m.return_value = {"elements": []}
        conn = OSMConnector()
        ok = await conn.health_check()
        assert ok is True
