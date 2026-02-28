"""Finland pilot configuration."""

from citysense.geo.bbox import BBox
from citysense.pilot.base import PilotConfig

HELSINKI_BBOX = BBox(west=24.80, south=60.10, east=25.30, north=60.35)

FI_CONFIG = PilotConfig(
    country="fi",
    language="fi",
    national_crs="EPSG:3067",
    default_cities={"Helsinki": HELSINKI_BBOX},
    connector_priority=("hri_fi", "mml", "osm", "mapillary_v4", "cdse_sentinel2"),
    wuf13_primary_dimensions=("resilience", "equity", "governance"),
    data_gaps={"informal_settlements": "Not applicable; use tenure from registers"},
    informality_heuristic=False,
)
