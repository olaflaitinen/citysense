# MCP Integration

## Cursor

Create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "citysense": {
      "command": "citysense",
      "args": ["serve", "--transport", "stdio"],
      "env": {
        "CITYSENSE_PILOT_COUNTRY": "fi",
        "CITYSENSE_VECTOR_STORE_URL": "http://localhost:6333",
        "MAPILLARY_ACCESS_TOKEN": "your_token",
        "CDSE_CLIENT_ID": "your_id",
        "CDSE_CLIENT_SECRET": "your_secret"
      }
    }
  }
}
```

## Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "citysense": {
      "command": "citysense",
      "args": ["serve", "--transport", "stdio"],
      "env": {
        "CITYSENSE_PILOT_COUNTRY": "az",
        "CITYSENSE_VECTOR_STORE_URL": "http://localhost:6333"
      }
    }
  }
}
```
