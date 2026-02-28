"""Pydantic v2 schema validators and GeoJSON validators."""

from typing import Any

from pydantic import BaseModel, field_validator


class GeoJSONGeometry(BaseModel):
    """GeoJSON geometry schema."""

    type: str
    coordinates: Any

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate geometry type."""
        allowed = {
            "Point",
            "LineString",
            "Polygon",
            "MultiPoint",
            "MultiLineString",
            "MultiPolygon",
        }
        if v not in allowed:
            msg = f"Invalid geometry type: {v}"
            raise ValueError(msg)
        return v
