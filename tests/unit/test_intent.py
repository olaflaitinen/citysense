"""Unit tests for intent parser."""

from citysense.rag.intent import parse_intent


def test_parse_helsinki_metro() -> None:
    """Test Helsinki metro query parsing."""
    intent = parse_intent("social housing zones within 1 km of metro stations in Helsinki")
    assert "metro_station" in intent.entity_types or "residential" in intent.entity_types
    assert intent.city_scope == "Helsinki"
    assert intent.country_scope == "fi"


def test_parse_baku() -> None:
    """Test Baku query parsing."""
    intent = parse_intent("housing zones in Baku")
    assert intent.city_scope == "Baku"
    assert intent.country_scope == "az"


def test_parse_stockholm() -> None:
    """Test Stockholm query parsing."""
    intent = parse_intent("parks in Stockholm")
    assert intent.city_scope == "Stockholm"
    assert intent.country_scope == "se"
    assert "park" in intent.entity_types or "building" in intent.entity_types


def test_parse_resilience() -> None:
    """Test WUF13 resilience dimension."""
    intent = parse_intent("areas with low resilience in Helsinki")
    assert intent.wuf13_dimension == "resilience"


def test_parse_equity() -> None:
    """Test WUF13 equity dimension."""
    intent = parse_intent("equity indicators in Baku")
    assert intent.wuf13_dimension == "equity"


def test_parse_sdg_transit() -> None:
    """Test SDG 11.2.1 transit indicator."""
    intent = parse_intent("transit accessible population in Copenhagen")
    assert intent.sdg_indicator == "11.2.1"


def test_parse_default_entity() -> None:
    """Test default entity type when no match."""
    intent = parse_intent("something random in Oslo")
    assert intent.entity_types
    assert intent.city_scope == "Oslo"
    assert intent.country_scope == "no"


def test_parse_bus_stop() -> None:
    """Test bus stop entity extraction."""
    intent = parse_intent("bus stops near parks in Helsinki")
    assert "bus_stop" in intent.entity_types
    assert "park" in intent.entity_types


def test_parse_railway() -> None:
    """Test railway station entity."""
    intent = parse_intent("train stations in Stockholm")
    assert "railway_station" in intent.entity_types


def test_parse_near_relation() -> None:
    """Test near spatial relation."""
    intent = parse_intent("housing near metro in Copenhagen")
    assert "near" in intent.spatial_relations or "near" in str(intent.spatial_relations)
