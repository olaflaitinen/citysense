# Contributing to CitySense

Thank you for your interest in contributing to CitySense. This document outlines the process and guidelines for contributions.

## Code of Conduct

This project adheres to the Contributor Covenant v2.1. By participating, you agree to uphold this code. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## How to Contribute

### Reporting Bugs

Use the [GitHub issue tracker](https://github.com/olaflaitinen/citysense/issues) with the bug report template. Include:

- CitySense version and Python version
- Steps to reproduce
- Expected vs actual behaviour
- Relevant logs or error messages

### Suggesting Features

Open a feature request issue. Describe the use case, proposed behaviour, and how it aligns with CitySense goals (WUF13, SDG 11, urban AI development).

### Pull Requests

1. Fork the repository and create a branch from `main`
2. Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages
3. Ensure tests pass: `pytest tests/`
4. Run linting: `ruff check src tests && ruff format --check src tests`
5. Run type checking: `mypy src/citysense`
6. Submit a pull request with a clear description

### Commit Message Format

| Type | Version Bump | Example |
|------|---------------|---------|
| feat: | Minor | feat(imagery): add Sentinel-3 LST connector |
| fix: | Patch | fix(rag): correct H3 pre-filter for antimeridian |
| feat!: | Major | feat!: remove deprecated search() method |
| docs:, chore:, test: | None | docs: add Baku pilot tutorial |

## Development Setup

```bash
git clone https://github.com/olaflaitinen/citysense.git
cd citysense
pip install -e ".[dev,clip]"
pre-commit install
```

## Priority Contribution Areas

- Additional country connectors for WUF13-relevant cities
- Non-Latin script handling (Arabic, Cyrillic for Azerbaijan and Central Asia)
- Informal settlement detection model improvements
- Climate adaptation document parsers for national plans

## License

By contributing, you agree that your contributions will be licensed under the EUPL-1.2.
