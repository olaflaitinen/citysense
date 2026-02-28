#!/bin/bash
# PyPI release script. Run from project root.
# Requires: pip install build twine
set -e
rm -rf dist/
python -m build
twine check dist/*
echo "Upload with: twine upload dist/*"
