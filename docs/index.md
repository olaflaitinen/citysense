# CitySense Documentation

Geospatial RAG and MCP Server Library for Urban AI Development.

Specification v0.2.0 | February 2026 | WUF13 Aligned

## Overview

CitySense bridges geospatial urban data with LLM toolchains through:

1. Geospatial RAG framework
2. Model Context Protocol (MCP) server

## Mathematical Foundations

### Spectral Indices

| Index | Formula | Range |
|-------|---------|-------|
| NDVI | $\frac{B_{08} - B_{04}}{B_{08} + B_{04}}$ | $[-1, +1]$ |
| NDWI | $\frac{B_{03} - B_{08}}{B_{03} + B_{08}}$ | $[-1, +1]$ |
| NDBI | $\frac{B_{11} - B_{08}}{B_{11} + B_{08}}$ | $[-1, +1]$ |

### Reciprocal Rank Fusion

$$\text{RRF}(d) = \sum_{R \in \{R_{\text{dense}}, R_{\text{sparse}}\}} \frac{1}{k + \text{rank}_R(d)}$$

with $k = 60$.

### Urban Resilience Composite Score

$$\text{URCS}(c) = \sum_{d \in D} w_d \cdot R_d(c)$$

where $D = \{\text{physical}, \text{climate}, \text{social}, \text{infrastructure}\}$.

## Pilot Countries

| Country | CRS | Primary City |
|---------|-----|--------------|
| Azerbaijan | EPSG:32638 | Baku |
| Finland | EPSG:3067 | Helsinki |
| Sweden | EPSG:3006 | Stockholm |
| Denmark | EPSG:25832 | Copenhagen |
| Norway | EPSG:25833 | Oslo |
