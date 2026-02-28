"""Unit tests for Urban Resilience Composite Score."""

from citysense.climate.resilience import compute_physical_resilience, compute_urcs


def test_urcs() -> None:
    """Test URCS computation."""
    score = compute_urcs(0.8, 0.7, 0.6, 0.9)
    assert 0 <= score <= 1
    assert score > 0.7


def test_physical_resilience() -> None:
    """Test physical resilience sub-dimension."""
    r = compute_physical_resilience(0.8, 0.2, 0.1)
    assert 0 <= r <= 1
