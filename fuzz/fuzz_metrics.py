"""Fuzz target for citysense.climate.resilience and citysense.urban.sdg11."""

import sys

import atheris


def test_one_input(data: bytes) -> None:
    """Fuzz URCS, physical resilience, and SDG 11 computations."""
    if len(data) < 48:
        return
    fdp = atheris.FuzzedDataProvider(data)

    try:
        from citysense.climate.resilience import (
            compute_physical_resilience,
            compute_urcs,
        )
        from citysense.urban.sdg11 import (
            compute_land_consumption_rate,
            compute_population_growth_rate,
            compute_sdg_1131,
        )

        physical = fdp.ConsumeFloatInRange(-1.0, 2.0)
        climate = fdp.ConsumeFloatInRange(-1.0, 2.0)
        social = fdp.ConsumeFloatInRange(-1.0, 2.0)
        infrastructure = fdp.ConsumeFloatInRange(-1.0, 2.0)
        urcs = compute_urcs(physical, climate, social, infrastructure)
        assert 0.0 <= urcs <= 1.0

        street = fdp.ConsumeFloatInRange(-1.0, 2.0)
        age = fdp.ConsumeFloatInRange(-1.0, 2.0)
        informal = fdp.ConsumeFloatInRange(-1.0, 2.0)
        pr = compute_physical_resilience(street, age, informal)
        assert 0.0 <= pr <= 1.0

        land_t0 = fdp.ConsumeFloatInRange(-100.0, 10000.0)
        land_t1 = fdp.ConsumeFloatInRange(-100.0, 10000.0)
        pop_t0 = fdp.ConsumeFloatInRange(-100.0, 1e7)
        pop_t1 = fdp.ConsumeFloatInRange(-100.0, 1e7)
        years = fdp.ConsumeFloatInRange(-10.0, 100.0)

        _ = compute_land_consumption_rate(land_t0, land_t1, years)
        _ = compute_population_growth_rate(pop_t0, pop_t1, years)
        _ = compute_sdg_1131(land_t0, land_t1, pop_t0, pop_t1, years)
    except (ValueError, ZeroDivisionError, OverflowError):
        pass


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
