"""CRS normalisation and transformation.

Handles CRS diversity across pilot countries:

| Country   | National CRS      | EPSG Code | Used For                    |
|-----------|-------------------|-----------|-----------------------------|
| Azerbaijan| UTM Zone 38N      | 32638     | Cadastral data (SCUPA)      |
| Finland   | ETRS89-TM35FIN    | 3067      | National topographic       |
| Sweden    | SWEREF99 TM       | 3006      | National topographic       |
| Denmark   | ETRS89 UTM32N     | 25832     | Cadastral and buildings    |
| Norway    | EUREF89 UTM33     | 25833     | National mapping           |

Uses pyproj.Transformer with always_xy=True for consistent axis order.
"""

from typing import TYPE_CHECKING

import geopandas as gpd

if TYPE_CHECKING:
    pass

_COUNTRY_CRS: dict[str, str] = {
    "az": "EPSG:32638",
    "fi": "EPSG:3067",
    "se": "EPSG:3006",
    "dk": "EPSG:25832",
    "no": "EPSG:25833",
}


def get_national_crs(country: str) -> str:
    """Get national CRS for pilot country.

    Args:
        country: ISO2 country code (az, fi, se, dk, no).

    Returns:
        EPSG string for national CRS.
    """
    return _COUNTRY_CRS.get(country.lower(), "EPSG:4326")


def normalize(
    gdf: gpd.GeoDataFrame,
    target: str = "EPSG:4326",
) -> gpd.GeoDataFrame:
    """Normalise GeoDataFrame to target CRS.

    Args:
        gdf: Input GeoDataFrame (any CRS).
        target: Target CRS (default WGS84).

    Returns:
        GeoDataFrame in target CRS.
    """
    if gdf.crs is None:
        msg = "GeoDataFrame has no CRS"
        raise ValueError(msg)
    if str(gdf.crs) == target:
        return gdf.copy()
    return gdf.to_crs(target)
