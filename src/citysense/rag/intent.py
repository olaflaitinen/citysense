"""NL intent parser producing SpatialIntent dataclass."""

from dataclasses import dataclass

from citysense.geo.bbox import BBox


@dataclass(frozen=True)
class SpatialIntent:
    """Parsed spatial query intent.

    Attributes:
        entity_types: OSM-style feature types (e.g. bus_stop, railway_station).
        spatial_relations: Relations (e.g. near, within_500m).
        attributes: Attribute filters (e.g. resilience: low).
        country_scope: ISO2 country code.
        city_scope: City name.
        bbox: Resolved bounding box (from city_scope if None).
        wuf13_dimension: WUF13 dialogue dimension.
        sdg_indicator: SDG indicator code (e.g. 11.2.1).
    """

    entity_types: tuple[str, ...]
    spatial_relations: tuple[str, ...]
    attributes: dict[str, str]
    country_scope: str | None
    city_scope: str | None
    bbox: BBox | None
    wuf13_dimension: str | None
    sdg_indicator: str | None


def parse_intent(query: str) -> SpatialIntent:
    """Parse natural language query into SpatialIntent.

    Rule-based extraction. LLM-assisted parsing can be added later.

    Args:
        query: Natural language query string.

    Returns:
        SpatialIntent with extracted slots.
    """
    q_lower = query.lower().strip()
    entity_types: list[str] = []
    spatial_relations: list[str] = []
    attributes: dict[str, str] = {}
    country_scope: str | None = None
    city_scope: str | None = None
    bbox: BBox | None = None
    wuf13_dimension: str | None = None
    sdg_indicator: str | None = None

    # Entity type keywords
    if "bus" in q_lower or "bus stop" in q_lower:
        entity_types.append("bus_stop")
    if "metro" in q_lower or "subway" in q_lower:
        entity_types.append("metro_station")
    if "railway" in q_lower or "train" in q_lower:
        entity_types.append("railway_station")
    if "housing" in q_lower or "social housing" in q_lower:
        entity_types.append("residential")
    if "park" in q_lower or "green" in q_lower:
        entity_types.append("park")

    # Spatial relations
    if "within" in q_lower and "km" in q_lower:
        spatial_relations.append("within_radius")
    if "near" in q_lower:
        spatial_relations.append("near")

    # City/country extraction (simplified)
    cities = ["helsinki", "baku", "stockholm", "copenhagen", "oslo"]
    for c in cities:
        if c in q_lower:
            city_scope = c.title()
            break
    countries = {
        "helsinki": "fi",
        "baku": "az",
        "stockholm": "se",
        "copenhagen": "dk",
        "oslo": "no",
    }
    if city_scope:
        country_scope = countries.get(city_scope.lower(), "fi")

    # WUF13 / SDG
    if "resilience" in q_lower:
        wuf13_dimension = "resilience"
    if "equity" in q_lower:
        wuf13_dimension = "equity"
    if "11.2.1" in query or "transit" in q_lower:
        sdg_indicator = "11.2.1"

    return SpatialIntent(
        entity_types=tuple(entity_types or ["building"]),
        spatial_relations=tuple(spatial_relations),
        attributes=attributes,
        country_scope=country_scope,
        city_scope=city_scope,
        bbox=bbox,
        wuf13_dimension=wuf13_dimension,
        sdg_indicator=sdg_indicator,
    )
