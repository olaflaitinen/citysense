# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- License: Apache 2.0 to EUPL-1.2

### Added

- Initial project structure per CitySense Specification v0.2.0
- Core module: config, session, exceptions, logging, registry
- Geo module: CRS, H3, bbox, geometry, OSM, raster utilities
- RAG pipeline: intent parsing, hybrid retriever, reranker, assembler
- MCP server with FastMCP and tool registry
- Connectors: base, OSM, Mapillary, KartaView, Sentinel CDSE
- Imagery: street and satellite processing modules
- Urban, housing, climate, governance, pilot modules
- CLI: init, index, query, serve, pilot, export, imagery, watch
- GitHub Actions CI workflow
- MkDocs documentation structure

## [0.2.0] - 2026-02-28

### Added

- WUF13 alignment and SDG 11 indicator coverage
- Five pilot country profiles: Azerbaijan, Finland, Sweden, Denmark, Norway
- Mathematical foundations: spectral indices, retrieval scoring, URCS, segregation indices
- Transit accessibility score (SDG 11.2.1)
- Land consumption rate (SDG 11.3.1)
- MCP tool registry: query_spatial_context, analyze_housing_zone, get_resilience_score, and others
- Resource registry: country profiles, WUF13 indicators, spectral indices
- Data standards and normalised GeoDataFrame schema
