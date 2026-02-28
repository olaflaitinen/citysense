"""Unit tests for spectral indices."""

import numpy as np
import pytest

from citysense.imagery.satellite.indices import (
    compute_index,
    compute_ndbi,
    compute_ndvi,
    compute_ndwi,
)


def test_compute_ndvi() -> None:
    """Test NDVI computation."""
    b04 = np.array([0.1, 0.2, 0.3], dtype=np.float32)
    b08 = np.array([0.3, 0.4, 0.5], dtype=np.float32)
    out = compute_ndvi(b04, b08)
    assert out.shape == (3,)
    assert np.all(out >= -1) and np.all(out <= 1)


def test_compute_ndvi_zero_denominator() -> None:
    """Test NDVI with zero sum bands."""
    b04 = np.array([0.0])
    b08 = np.array([0.0])
    out = compute_ndvi(b04, b08)
    assert not np.any(np.isnan(out))


def test_compute_ndwi() -> None:
    """Test NDWI computation."""
    b03 = np.array([0.2, 0.3], dtype=np.float32)
    b08 = np.array([0.1, 0.2], dtype=np.float32)
    out = compute_ndwi(b03, b08)
    assert out.shape == (2,)


def test_compute_ndbi() -> None:
    """Test NDBI computation."""
    b08 = np.array([0.2], dtype=np.float32)
    b11 = np.array([0.3], dtype=np.float32)
    out = compute_ndbi(b08, b11)
    assert out.shape == (1,)


def test_compute_index_ndvi() -> None:
    """Test compute_index for NDVI."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.1]),
        "B04": np.array([0.2]),
        "B08": np.array([0.4]),
        "B11": np.array([0.2]),
    }
    out = compute_index("NDVI", bands)
    assert out.dtype == np.float32


def test_compute_index_ndwi() -> None:
    """Test compute_index for NDWI."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.3]),
        "B04": np.array([0.2]),
        "B08": np.array([0.1]),
        "B11": np.array([0.2]),
    }
    out = compute_index("NDWI", bands)
    assert out.dtype == np.float32


def test_compute_index_ndbi() -> None:
    """Test compute_index for NDBI."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.1]),
        "B04": np.array([0.2]),
        "B08": np.array([0.2]),
        "B11": np.array([0.3]),
    }
    out = compute_index("NDBI", bands)
    assert out.dtype == np.float32


def test_compute_index_evi() -> None:
    """Test compute_index for EVI."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.1]),
        "B04": np.array([0.2]),
        "B08": np.array([0.4]),
        "B11": np.array([0.2]),
    }
    out = compute_index("EVI", bands)
    assert out.dtype == np.float32


def test_compute_index_mndwi() -> None:
    """Test compute_index for MNDWI."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.3]),
        "B04": np.array([0.2]),
        "B08": np.array([0.1]),
        "B11": np.array([0.2]),
    }
    out = compute_index("MNDWI", bands)
    assert out.dtype == np.float32


def test_compute_index_bsi() -> None:
    """Test compute_index for BSI."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.1]),
        "B04": np.array([0.2]),
        "B08": np.array([0.3]),
        "B11": np.array([0.4]),
    }
    out = compute_index("BSI", bands)
    assert out.dtype == np.float32


def test_compute_index_unknown() -> None:
    """Test compute_index with unknown index raises."""
    bands = {
        "B02": np.array([0.1]),
        "B03": np.array([0.1]),
        "B04": np.array([0.2]),
        "B08": np.array([0.3]),
        "B11": np.array([0.4]),
    }
    with pytest.raises(ValueError, match="Unknown index"):
        compute_index("UNKNOWN", bands)
