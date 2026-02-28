"""Configuration via pydantic-settings BaseSettings.

Configuration is read in priority order: (1) environment variables,
(2) citysense.toml at the project root, (3) defaults.
All fields are immutable after construction.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CitySenseConfig(BaseSettings):
    """CitySense runtime configuration.

    All fields use CITYSENSE_ prefix when set via environment variables.
    """

    model_config = SettingsConfigDict(
        env_prefix="CITYSENSE_",
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
    )

    # Runtime
    pilot_country: Literal["az", "fi", "se", "dk", "no"] | None = None
    log_level: str = "INFO"
    cache_dir: Path = Path(".citysense_cache")

    # Vector store (Qdrant 1.17.x)
    vector_store_backend: Literal["qdrant", "pgvector"] = "qdrant"
    vector_store_url: str = "http://localhost:6333"
    vector_store_collection_prefix: str = "cs"

    # Text embedding (fastembed 0.4.2 with ONNX runtime)
    embedding_model: str = "BAAI/bge-m3"
    embedding_dim: int = 1024
    sparse_embedding_model: str = "Qdrant/bm25"

    # Vision embedding (CLIP ViT-B/32 via transformers 4.48.3)
    clip_model: str = "openai/clip-vit-base-patch32"
    clip_dim: int = 512
    clip_enabled: bool = True

    # LLM (routed through LiteLLM 1.57.x)
    llm_model: str = "claude-sonnet-4-6"
    llm_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")

    # Spatial
    default_crs: str = "EPSG:4326"
    h3_resolution_fine: int = 9
    h3_resolution_coarse: int = 7

    # MCP server (mcp 1.4.x FastMCP)
    mcp_host: str = "127.0.0.1"
    mcp_port: int = 7832
    mcp_transport: Literal["stdio", "sse"] = "stdio"

    # Mapillary API v4
    mapillary_access_token: str | None = None
    mapillary_max_images_per_bbox: int = 50
    mapillary_min_captured_at: str | None = None

    # KartaView
    kartatview_base_url: str = "https://kartaview.org/api"
    kartatview_max_photos_per_page: int = 100

    # Copernicus Data Space Ecosystem
    cdse_client_id: str | None = None
    cdse_client_secret: str | None = None
    cdse_stac_url: str = "https://stac.dataspace.copernicus.eu"
    cdse_odata_url: str = "https://catalogue.dataspace.copernicus.eu/odata/v1"
    cdse_download_url: str = "https://download.dataspace.copernicus.eu/odata/v1"
    cdse_s2_max_cloud_cover: float = 20.0
    cdse_s2_level: Literal["L1C", "L2A"] = "L2A"
    cdse_s1_polarization: Literal["VV", "VH", "VV+VH"] = "VV+VH"

    # Sentinel Hub Process API
    sentinel_hub_base_url: str = "https://services.sentinel-hub.com"
    sentinel_hub_client_id: str | None = None
    sentinel_hub_client_secret: str | None = None

    # Imagery processing
    satellite_tile_cache_dir: Path = Path(".citysense_cache/satellite")
    street_imagery_cache_dir: Path = Path(".citysense_cache/street")
    max_satellite_tile_size_mb: float = 200.0

    # Realtime watcher (APScheduler 3.11.x)
    realtime_poll_interval_s: int = 3600
    realtime_s2_revisit_days: int = 5
    realtime_ndvi_change_threshold: float = 0.15
    realtime_sar_change_threshold_db: float = 3.0
