# Installation

## Requirements

- Python 3.12 or 3.13
- GDAL 3.10+ (for rasterio, geopandas)

## pip

```bash
pip install citysense
```

Optional extras:

| Extra | Purpose |
|-------|---------|
| clip | CLIP ViT-B/32 for street imagery embedding |
| sentinelhub | Sentinel Hub Process API |
| dev | ruff, mypy, pytest, mkdocs |

## conda-forge

For binary compatibility with GDAL, PROJ, GEOS:

```bash
conda env create -f environment.yml
conda activate citysense
pip install -e ".[dev]"
```

## Editable Install

```bash
git clone https://github.com/olaflaitinen/citysense.git
cd citysense
pip install -e ".[dev]"
```
