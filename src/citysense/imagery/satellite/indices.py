"""Spectral index computation (NDVI, NDWI, NDBI, EVI, MNDWI, BSI).

Formulas per Section 8.1:

- NDVI: $\\frac{B_{08} - B_{04}}{B_{08} + B_{04}}$
- NDWI: $\\frac{B_{03} - B_{08}}{B_{03} + B_{08}}$
- NDBI: $\\frac{B_{11} - B_{08}}{B_{11} + B_{08}}$
- EVI: $2.5 \\cdot \\frac{B_{08} - B_{04}}{B_{08} + 6 \\cdot B_{04} - 7.5 \\cdot B_{02} + 1}$
- MNDWI: $\\frac{B_{03} - B_{11}}{B_{03} + B_{11}}$
- BSI: $\\frac{(B_{11} + B_{04}) - (B_{08} + B_{02})}{(B_{11} + B_{04}) + (B_{08} + B_{02})}$
"""

from typing import Any, Literal, cast

import numpy as np
from numpy.typing import NDArray


def compute_ndvi(b04: NDArray[Any], b08: NDArray[Any]) -> NDArray[Any]:
    """Compute NDVI from Red and NIR bands."""
    out = (b08 - b04) / np.where(b08 + b04 == 0, 1e-10, b08 + b04)
    return cast(NDArray[Any], out)


def compute_ndwi(b03: NDArray[Any], b08: NDArray[Any]) -> NDArray[Any]:
    """Compute NDWI (McFeeters 1996) from Green and NIR bands."""
    out = (b03 - b08) / np.where(b03 + b08 == 0, 1e-10, b03 + b08)
    return cast(NDArray[Any], out)


def compute_ndbi(b08: NDArray[Any], b11: NDArray[Any]) -> NDArray[Any]:
    """Compute NDBI (Zha et al. 2003) from NIR and SWIR1 bands."""
    out = (b11 - b08) / np.where(b11 + b08 == 0, 1e-10, b11 + b08)
    return cast(NDArray[Any], out)


def compute_index(
    index: Literal["NDVI", "NDWI", "NDBI", "EVI", "MNDWI", "BSI"],
    bands: dict[str, NDArray[Any]],
) -> NDArray[Any]:
    """Compute spectral index from band dict.

    Args:
        index: Index identifier.
        bands: Dict with keys B02, B03, B04, B08, B11 (and B12 for BSI).

    Returns:
        Float32 array of index values.
    """
    if index == "NDVI":
        out = compute_ndvi(bands["B04"], bands["B08"]).astype(np.float32)
        return cast(NDArray[Any], out)
    if index == "NDWI":
        out = compute_ndwi(bands["B03"], bands["B08"]).astype(np.float32)
        return cast(NDArray[Any], out)
    if index == "NDBI":
        out = compute_ndbi(bands["B08"], bands["B11"]).astype(np.float32)
        return cast(NDArray[Any], out)
    if index == "EVI":
        out = (
            2.5
            * (bands["B08"] - bands["B04"])
            / (bands["B08"] + 6 * bands["B04"] - 7.5 * bands["B02"] + 1 + 1e-10)
        ).astype(np.float32)
        return cast(NDArray[Any], out)
    if index == "MNDWI":
        out = (bands["B03"] - bands["B11"]) / np.where(
            bands["B03"] + bands["B11"] == 0, 1e-10, bands["B03"] + bands["B11"]
        )
        return cast(NDArray[Any], out.astype(np.float32))
    if index == "BSI":
        num = (bands["B11"] + bands["B04"]) - (bands["B08"] + bands["B02"])
        den = (bands["B11"] + bands["B04"]) + (bands["B08"] + bands["B02"])
        out = (num / np.where(den == 0, 1e-10, den)).astype(np.float32)
        return cast(NDArray[Any], out)
    msg = f"Unknown index: {index}"
    raise ValueError(msg)
