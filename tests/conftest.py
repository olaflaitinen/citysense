"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add src to path for editable install compatibility
src = Path(__file__).resolve().parent.parent / "src"
if str(src) not in sys.path:
    sys.path.insert(0, str(src))
