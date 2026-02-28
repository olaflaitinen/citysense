"""Per-request context: pilot, bbox, trace_id."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from citysense.geo.bbox import BBox


@dataclass
class SessionContext:
    """Per-request session context.

    Attributes:
        pilot_country: ISO2 country code (az, fi, se, dk, no).
        bbox: Active bounding box for spatial queries.
        trace_id: Request trace ID for distributed tracing.
        metadata: Additional request metadata.
    """

    pilot_country: str | None = None
    bbox: BBox | None = None
    trace_id: str | None = None
    metadata: dict[str, Any] | None = None
