"""Abstract PilotConfig for country-specific settings."""

from dataclasses import dataclass

from citysense.geo.bbox import BBox


@dataclass(frozen=True)
class PilotConfig:
    """Pilot country configuration.

    Attributes:
        country: ISO2 code.
        language: IETF BCP 47 tag.
        national_crs: EPSG string.
        default_cities: City name to BBox mapping.
        connector_priority: Ordered connector IDs.
        wuf13_primary_dimensions: WUF13 dimension tags.
        data_gaps: Known gaps and fallback strategies.
        informality_heuristic: Use SAR/spectral heuristic for tenure.
    """

    country: str
    language: str
    national_crs: str
    default_cities: dict[str, BBox]
    connector_priority: tuple[str, ...]
    wuf13_primary_dimensions: tuple[str, ...]
    data_gaps: dict[str, str]
    informality_heuristic: bool
