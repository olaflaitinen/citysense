"""Unit tests for session context."""

from citysense.core.session import SessionContext
from citysense.geo.bbox import BBox


def test_session_context_defaults() -> None:
    """Test SessionContext defaults."""
    ctx = SessionContext()
    assert ctx.pilot_country is None
    assert ctx.bbox is None
    assert ctx.trace_id is None
    assert ctx.metadata is None


def test_session_context_with_bbox() -> None:
    """Test SessionContext with bbox."""
    bbox = BBox(west=24.9, south=60.1, east=25.0, north=60.2)
    ctx = SessionContext(pilot_country="fi", bbox=bbox, trace_id="abc")
    assert ctx.pilot_country == "fi"
    assert ctx.bbox == bbox
    assert ctx.trace_id == "abc"
