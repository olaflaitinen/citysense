"""Shapely 2.1.2 operation wrappers with type annotations."""

from typing import Any

from shapely.geometry import Point
from shapely.ops import transform
from shapely.validation import make_valid


def buffer_metres(geom: Any, distance_m: float, crs_epsg: int = 4326) -> Any:
    """Buffer geometry by distance in metres.

    For EPSG:4326, uses approximate conversion. For projected CRS,
    uses native units.

    Args:
        geom: Shapely geometry.
        distance_m: Buffer distance in metres.
        crs_epsg: CRS of input geometry.

    Returns:
        Buffered geometry.
    """
    if crs_epsg == 4326:
        import pyproj

        proj = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        geom_proj = transform(proj.transform, geom)
        buffered = geom_proj.buffer(distance_m)
        proj_inv = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
        return transform(proj_inv.transform, buffered)
    return geom.buffer(distance_m)


def centroid(geom: Any) -> Point | None:
    """Get centroid of geometry.

    Args:
        geom: Shapely geometry.

    Returns:
        Centroid point or None for empty.
    """
    c = geom.centroid
    return c if not c.is_empty else None


def make_valid_geometry(geom: Any) -> Any:
    """Repair invalid geometry.

    Args:
        geom: Potentially invalid Shapely geometry.

    Returns:
        Valid geometry.
    """
    return make_valid(geom)
