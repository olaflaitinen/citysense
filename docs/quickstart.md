# Quick Start

## Installation

```bash
pip install citysense
```

With CLIP vision embedding support:

```bash
pip install "citysense[clip]"
```

## Initialisation

```bash
citysense pilot init fi
```

## Build Index

```bash
citysense index build --city Helsinki --sources osm
```

## Query

```bash
citysense query "social housing zones within 1 km of metro stations in Helsinki"
```

## MCP Server

```bash
citysense serve --transport stdio
```

Configure in Cursor or Claude Desktop per the MCP integration guide.
