"""Unit tests for SDG 11 indicators."""

import math

from citysense.urban.sdg11 import (
    compute_land_consumption_rate,
    compute_population_growth_rate,
    compute_sdg_1131,
    compute_transit_accessible_proportion,
)


def test_land_consumption_rate() -> None:
    """Test LCR computation."""
    lcr = compute_land_consumption_rate(100.0, 120.0, 5.0)
    assert lcr > 0
    assert abs(lcr - (math.log(1.2) / 5)) < 1e-10


def test_population_growth_rate() -> None:
    """Test PGR computation."""
    pgr = compute_population_growth_rate(1000.0, 1100.0, 5.0)
    assert pgr > 0


def test_sdg_1131() -> None:
    """Test SDG 11.3.1 ratio."""
    ratio = compute_sdg_1131(100.0, 120.0, 1000.0, 1100.0, 5.0)
    assert ratio > 0


def test_transit_accessible_proportion() -> None:
    """Test SDG 11.2.1 proportion."""
    pop = {"c1": 100, "c2": 200, "c3": 300}
    accessible = {"c1", "c3"}
    p = compute_transit_accessible_proportion(pop, accessible)
    assert abs(p - 400 / 600) < 1e-10


def test_land_consumption_rate_zero_input() -> None:
    """Test LCR with zero urban land returns 0."""
    assert compute_land_consumption_rate(0, 120, 5) == 0.0
    assert compute_land_consumption_rate(100, 120, 0) == 0.0


def test_population_growth_rate_zero_input() -> None:
    """Test PGR with zero population returns 0."""
    assert compute_population_growth_rate(0, 1100, 5) == 0.0
    assert compute_population_growth_rate(1000, 1100, 0) == 0.0


def test_sdg_1131_zero_pgr() -> None:
    """Test SDG 11.3.1 with zero PGR returns 0."""
    assert compute_sdg_1131(100, 120, 1000, 1000, 5) == 0.0


def test_transit_accessible_proportion_empty() -> None:
    """Test SDG 11.2.1 with zero total population returns 0."""
    assert compute_transit_accessible_proportion({}, set()) == 0.0
    assert compute_transit_accessible_proportion({"c1": 0}, {"c1"}) == 0.0
