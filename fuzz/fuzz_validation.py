"""Fuzz target for citysense.utils.validation.GeoJSONGeometry."""

import sys

import atheris


def test_one_input(data: bytes) -> None:
    """Fuzz GeoJSON geometry validation."""
    fdp = atheris.FuzzedDataProvider(data)
    geom_type = fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 50))
    try:
        from citysense.utils.validation import GeoJSONGeometry

        GeoJSONGeometry(type=geom_type, coordinates=[])
    except (ValueError, TypeError):
        pass


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
