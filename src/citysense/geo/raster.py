"""rasterio 1.4.x read/write with windowed read and COG write."""

from pathlib import Path
from typing import Any

import rasterio
from numpy.typing import NDArray
from rasterio.windows import from_bounds


def read_window(
    path: Path | str,
    bbox_xy: tuple[float, float, float, float],
    bands: list[int] | None = None,
) -> tuple[NDArray[Any], dict[str, Any]]:
    """Read raster window by bounding box (in raster CRS).

    Args:
        path: Path to raster file.
        bbox_xy: (minx, miny, maxx, maxy) in raster CRS.
        bands: Band indices (1-based). None for all.

    Returns:
        (data array, profile dict) tuple.
    """
    with rasterio.open(path) as src:
        window = from_bounds(*bbox_xy, transform=src.transform)
        band_list = bands or list(range(1, src.count + 1))
        data = src.read(band_list, window=window)
        transform = rasterio.windows.transform(window, src.transform)
        profile = src.profile.copy()
        profile.update(
            width=window.width,
            height=window.height,
            transform=transform,
            count=len(band_list),
        )
    return data, profile
