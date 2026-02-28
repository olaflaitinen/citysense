"""Fuzz target for citysense.geo.bbox.BBox."""

import sys

import atheris


def test_one_input(data: bytes) -> None:
    """Fuzz BBox creation, intersection, and expansion."""
    if len(data) < 40:
        return
    fdp = atheris.FuzzedDataProvider(data)
    west = fdp.ConsumeFloatInRange(-180.0, 180.0)
    south = fdp.ConsumeFloatInRange(-90.0, 90.0)
    east = fdp.ConsumeFloatInRange(-180.0, 180.0)
    north = fdp.ConsumeFloatInRange(-90.0, 90.0)

    try:
        from citysense.geo.bbox import BBox

        bbox = BBox(west=west, south=south, east=east, north=north)
        _ = bbox.area_km2
        _ = bbox.to_tuple()

        west2 = fdp.ConsumeFloatInRange(-180.0, 180.0)
        south2 = fdp.ConsumeFloatInRange(-90.0, 90.0)
        east2 = fdp.ConsumeFloatInRange(-180.0, 180.0)
        north2 = fdp.ConsumeFloatInRange(-90.0, 90.0)
        try:
            other = BBox(west=west2, south=south2, east=east2, north=north2)
            _ = bbox.intersection(other)
        except ValueError:
            pass

        factor = fdp.ConsumeFloatInRange(0.01, 10.0)
        _ = bbox.expand(factor)
    except (ValueError, OverflowError):
        pass


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
