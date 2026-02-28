<p align="center">
  <img src="docs/assets/logo.svg" alt="CitySense Logo" width="240"/>
</p>

# CitySense

[![Python](https://img.shields.io/badge/python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/citysense?logo=pypi&logoColor=white)](https://pypi.org/project/citysense/)
[![License](https://img.shields.io/badge/license-EUPL--1.2-green?logo=europeanunion&logoColor=white)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/olaflaitinen/citysense/ci.yml?branch=main&logo=githubactions&logoColor=white)](https://github.com/olaflaitinen/citysense/actions)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/olaflaitinen/citysense/badge)](https://scorecard.dev/viewer/?uri=github.com/olaflaitinen/citysense)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen?logo=codecov&logoColor=white)](https://github.com/olaflaitinen/citysense)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000?logo=ruff&logoColor=white)](https://docs.astral.sh/ruff/)
[![mypy](https://img.shields.io/badge/type%20checker-mypy-blue?logo=python&logoColor=white)](https://mypy-lang.org/)
[![Read the Docs](https://img.shields.io/readthedocs/citysense?logo=readthedocs&logoColor=white)](https://citysense.readthedocs.io)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Qdrant](https://img.shields.io/badge/vector%20store-Qdrant-0094FF?logo=qdrant&logoColor=white)](https://qdrant.tech/)
[![OpenStreetMap](https://img.shields.io/badge/data-OpenStreetMap-7EBC6F?logo=openstreetmap&logoColor=white)](https://www.openstreetmap.org/)
[![SDG 11](https://img.shields.io/badge/UN-SDG%2011-009EDB)](https://sdgs.un.org/goals/goal11)
[![MCP](https://img.shields.io/badge/protocol-MCP-6366F1)](https://modelcontextprotocol.io/)
[![Shapely](https://img.shields.io/badge/geometry-Shapely-2.1%2B-3776AB?logo=python&logoColor=white)](https://shapely.readthedocs.io/)
[![GeoPandas](https://img.shields.io/badge/geospatial-GeoPandas-1.1%2B-3776AB?logo=python&logoColor=white)](https://geopandas.org/)

**Geospatial RAG and MCP Server Library for Urban AI Development**

Specification v0.2.0 | February 2026 | WUF13 Aligned

---

## Overview

CitySense is an open-source Python library that bridges geospatial urban data with large language model (LLM) toolchains. It provides two tightly integrated components:

1. **Geospatial RAG framework** that semantically indexes spatial datasets and retrieves relevant context for natural language queries
2. **Model Context Protocol (MCP) server** that exposes city intelligence directly into AI-assisted development environments such as Cursor, VS Code with Continue extension, and Claude

The core design philosophy: a developer should be able to write a comment such as:

```python
# find housing zones with low resilience scores near transit corridors in Baku
```

and have CitySense resolve that intent into structured geospatial results drawn from live and indexed sources, with no spatial query code required from the developer.

CitySense adds a third observational layer on top of traditional vector geospatial data: street-level imagery via the Mapillary API v4 and KartaView REST API, and multispectral satellite imagery via the Copernicus Data Space Ecosystem (CDSE) and Sentinel Hub.

---

## Key Features

| Capability | Description |
|------------|-------------|
| Natural language queries | Intent parsing and semantic retrieval over geospatial knowledge bases |
| Multi-source indexing | OpenStreetMap, Sentinel-2, Mapillary, KartaView, national registers |
| MCP integration | Native Model Context Protocol server for Cursor, Claude, and VS Code |
| WUF13 alignment | Pilot countries (Azerbaijan, Finland, Sweden, Denmark, Norway) with consistent schemas |
| SDG 11 metrics | Land consumption rate (11.3.1), urban resilience composite score |
| Spectral indices | NDVI, NDWI, NDBI, EVI, BSI from Sentinel-2 L2A |
| Reciprocal Rank Fusion | Hybrid dense and sparse retrieval with configurable $k$ |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CitySense Stack                                  │
├─────────────────────────────────────────────────────────────────────────┤
│  CLI (citysense)                                                        │
│  pilot init | index build | query | serve                                │
├─────────────────────────────────────────────────────────────────────────┤
│  MCP Server (stdio/SSE)          │  Geospatial RAG                       │
│  Tools: query, describe, bounds  │  Intent → H3 filter → Dense+Sparse   │
├─────────────────────────────────────────────────────────────────────────┤
│  Connectors: OSM, Sentinel-2, Mapillary, KartaView, CDSE                 │
├─────────────────────────────────────────────────────────────────────────┤
│  Vector Store (Qdrant)  │  Geometry (Shapely, GeoPandas, H3)            │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Primary User Groups

| Group | Use Case |
|-------|----------|
| Urban AI Developers | Build applications on city data with semantic access to geospatial knowledge bases |
| Smart City Researchers | Query, compare, and analyze datasets across multiple countries with consistent schemas |
| Urban Policy Tools Builders | Prototype AI-assisted planning tools aligned with UN New Urban Agenda, SDG 11, and WUF13 |

---

## Requirements

- Python 3.12 or 3.13
- Qdrant (for vector store; default `http://localhost:6333`)

---

## Installation

```bash
pip install citysense
```

### Optional Extras

| Extra | Purpose |
|-------|---------|
| `clip` | CLIP ViT-B/32 for street imagery embedding |
| `sentinelhub` | Sentinel Hub Process API |
| `dev` | ruff, mypy, pytest, mkdocs |

```bash
pip install "citysense[clip]"
pip install "citysense[dev]"
```

For binary compatibility with GDAL, PROJ, GEOS:

```bash
conda env create -f environment.yml
conda activate citysense
pip install -e ".[dev]"
```

---

## Quick Start

```bash
citysense pilot init fi
citysense index build --city Helsinki --sources osm
citysense query "social housing zones within 1 km of metro stations in Helsinki"
citysense serve --transport stdio
```

---

## Pilot Countries

| Country | Module Key | National CRS | Primary City |
|---------|------------|--------------|--------------|
| Azerbaijan | `az` | EPSG:32638 | Baku |
| Finland | `fi` | EPSG:3067 | Helsinki |
| Sweden | `se` | EPSG:3006 | Stockholm |
| Denmark | `dk` | EPSG:25832 | Copenhagen |
| Norway | `no` | EPSG:25833 | Oslo |

---

## Mathematical Foundations

Spectral indices (NDVI, NDWI, NDBI), Reciprocal Rank Fusion, Urban Resilience Composite Score, SDG 11.3.1 Land Consumption Rate. Full reference: [docs/reference/mathematical-foundations.md](docs/reference/mathematical-foundations.md).

---

## License

EUPL-1.2. See [LICENSE](LICENSE).

---

## Links

| Resource | URL |
|----------|-----|
| Documentation | [citysense.readthedocs.io](https://citysense.readthedocs.io) |
| Repository | [github.com/olaflaitinen/citysense](https://github.com/olaflaitinen/citysense) |
| Issues | [github.com/olaflaitinen/citysense/issues](https://github.com/olaflaitinen/citysense/issues) |
| Changelog | [CHANGELOG.md](CHANGELOG.md) |
