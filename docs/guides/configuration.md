# Configuration

Configuration is read in priority order:

1. Environment variables (prefix `CITYSENSE_`)
2. `.env` file at project root
3. Defaults

## Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| CITYSENSE_PILOT_COUNTRY | None | az, fi, se, dk, no |
| CITYSENSE_VECTOR_STORE_URL | http://localhost:6333 | Qdrant URL |
| CITYSENSE_EMBEDDING_MODEL | BAAI/bge-m3 | Text embedding model |
| MAPILLARY_ACCESS_TOKEN | None | Mapillary API token |
| CDSE_CLIENT_ID | None | Copernicus Data Space client ID |
| CDSE_CLIENT_SECRET | None | Copernicus Data Space client secret |

## Example .env

```
CITYSENSE_PILOT_COUNTRY=fi
CITYSENSE_VECTOR_STORE_URL=http://localhost:6333
MAPILLARY_ACCESS_TOKEN=your_token
CDSE_CLIENT_ID=your_id
CDSE_CLIENT_SECRET=your_secret
```
