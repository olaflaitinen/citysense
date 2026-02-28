"""Core spatial layer: geometry, CRS, H3, raster."""

from citysense.geo.bbox import BBox
from citysense.geo.crs import normalize as normalize_crs
from citysense.geo.h3 import (
    bbox_to_h3_set,
    compact,
    h3_to_centroid,
    k_ring_buffer,
    polyfill,
)

__all__ = [
    "BBox",
    "normalize_crs",
    "polyfill",
    "k_ring_buffer",
    "compact",
    "h3_to_centroid",
    "bbox_to_h3_set",
]
