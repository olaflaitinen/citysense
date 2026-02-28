"""SDG 11 indicator computation.

SDG 11.3.1 Land Consumption Rate:
$$\\text{SDG}_{11.3.1} = \\frac{\\text{LCR}}{\\text{PGR}}$$

SDG 11.2.1 Transit accessibility (population-weighted proportion).
"""

import math


def compute_land_consumption_rate(
    urban_land_t0_km2: float,
    urban_land_t1_km2: float,
    years: float,
) -> float:
    """Compute Land Consumption Rate.

    $$\\text{LCR} = \\frac{\\ln(U_{\\text{land}}(t_1) / U_{\\text{land}}(t_0))}{t_1 - t_0}$$

    Args:
        urban_land_t0_km2: Urban land area at start (km^2).
        urban_land_t1_km2: Urban land area at end (km^2).
        years: Time interval in years.

    Returns:
        LCR value.
    """
    if urban_land_t0_km2 <= 0 or years <= 0:
        return 0.0
    return math.log(urban_land_t1_km2 / urban_land_t0_km2) / years


def compute_population_growth_rate(
    pop_t0: float,
    pop_t1: float,
    years: float,
) -> float:
    """Compute Population Growth Rate.

    $$\\text{PGR} = \\frac{\\ln(P(t_1) / P(t_0))}{t_1 - t_0}$$

    Args:
        pop_t0: Population at start.
        pop_t1: Population at end.
        years: Time interval in years.

    Returns:
        PGR value.
    """
    if pop_t0 <= 0 or years <= 0:
        return 0.0
    return math.log(pop_t1 / pop_t0) / years


def compute_sdg_1131(
    urban_land_t0_km2: float,
    urban_land_t1_km2: float,
    pop_t0: float,
    pop_t1: float,
    years: float,
) -> float:
    """Compute SDG 11.3.1 (land consumption to population growth ratio).

    Sustainable urban growth: ratio approximately 1.
    Ratio > 1: land consumption outpacing population growth.
    Ratio < 1: increasing density.

    Args:
        urban_land_t0_km2: Urban land at start.
        urban_land_t1_km2: Urban land at end.
        pop_t0: Population at start.
        pop_t1: Population at end.
        years: Time interval.

    Returns:
        SDG 11.3.1 ratio.
    """
    lcr = compute_land_consumption_rate(urban_land_t0_km2, urban_land_t1_km2, years)
    pgr = compute_population_growth_rate(pop_t0, pop_t1, years)
    if pgr == 0:
        return 0.0
    return lcr / pgr


def compute_transit_accessible_proportion(
    population_by_cell: dict[str, float],
    accessible_cells: set[str],
) -> float:
    """Compute SDG 11.2.1 (population with convenient transit access).

    $$\\text{SDG}_{11.2.1} = \\frac{\\sum_{c \\in C} p_c \\cdot
    \\mathbb{1}[A_{\\text{norm}}(c) \\geq 0.35]}{\\sum_{c \\in C} p_c}$$

    Args:
        population_by_cell: H3 cell to population mapping.
        accessible_cells: Set of transit-accessible H3 cell IDs.

    Returns:
        Proportion in [0, 1].
    """
    total = sum(population_by_cell.values())
    if total <= 0:
        return 0.0
    accessible_pop = sum(p for cell, p in population_by_cell.items() if cell in accessible_cells)
    return accessible_pop / total
