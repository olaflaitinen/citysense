"""Fuzz target for citysense.rag.intent.parse_intent."""

import sys

import atheris


def test_one_input(data: bytes) -> None:
    """Fuzz parse_intent with arbitrary byte strings."""
    fdp = atheris.FuzzedDataProvider(data)
    query = fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes())
    try:
        from citysense.rag.intent import parse_intent

        result = parse_intent(query)
        assert result.entity_types is not None
    except (ValueError, TypeError):
        pass


def main() -> None:
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
