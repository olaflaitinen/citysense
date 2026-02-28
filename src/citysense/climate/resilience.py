r"""Urban Resilience Composite Score (URCS).

$$\text{URCS}(c) = \sum_{d \in D} w_d \cdot R_d(c)$$

where $D = \{\text{physical}, \text{climate}, \text{social}, \text{infrastructure}\}$.
"""

DEFAULT_WEIGHTS = {
    "physical": 0.30,
    "climate": 0.30,
    "social": 0.20,
    "infrastructure": 0.20,
}


def compute_urcs(
    physical: float,
    climate: float,
    social: float,
    infrastructure: float,
    weights: dict[str, float] | None = None,
) -> float:
    """Compute Urban Resilience Composite Score.

    All sub-dimension scores must be in [0, 1]. Higher is more resilient.

    Args:
        physical: Physical resilience (street condition, housing age).
        climate: Climate resilience (inverse of flood/heat risk).
        social: Social resilience (income diversity, service access).
        infrastructure: Infrastructure resilience (transit, utilities).

    Returns:
        URCS in [0, 1].
    """
    w = weights or DEFAULT_WEIGHTS
    return (
        w.get("physical", 0.30) * max(0, min(1, physical))
        + w.get("climate", 0.30) * max(0, min(1, climate))
        + w.get("social", 0.20) * max(0, min(1, social))
        + w.get("infrastructure", 0.20) * max(0, min(1, infrastructure))
    )


def compute_physical_resilience(
    street_condition: float,
    building_age_norm: float,
    informality_score: float,
    alpha_s: float = 0.4,
    alpha_a: float = 0.35,
    alpha_sar: float = 0.25,
) -> float:
    r"""Compute physical resilience sub-dimension.

    $$R_{\text{physical}} = \alpha_s \cdot s_{\text{condition}}
    + \alpha_a \cdot (1 - a_{\text{norm}})
    + \alpha_{\text{SAR}} \cdot (1 - I_{\text{informal}})$$
    """
    return (
        alpha_s * max(0, min(1, street_condition))
        + alpha_a * (1 - max(0, min(1, building_age_norm)))
        + alpha_sar * (1 - max(0, min(1, informality_score)))
    )
