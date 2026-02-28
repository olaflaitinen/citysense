"""Azerbaijan pilot configuration (Baku focus)."""

from citysense.geo.bbox import BBox
from citysense.pilot.base import PilotConfig

BAKU_BBOX = BBox(west=49.70, south=40.30, east=50.10, north=40.55)

AZ_CONFIG = PilotConfig(
    country="az",
    language="az",
    national_crs="EPSG:32638",
    default_cities={"Baku": BAKU_BBOX},
    connector_priority=("scupa", "osm", "mapillary_v4", "kartatview", "cdse_sentinel2"),
    wuf13_primary_dimensions=("resilience", "equity", "tenure"),
    data_gaps={"peri_urban": "SAR texture + NDBI heuristic for informality"},
    informality_heuristic=True,
)
