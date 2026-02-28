# PyPI release script for Windows. Run from project root.
# Requires: pip install build twine
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build
twine check dist/*
Write-Host "Upload with: twine upload dist/*"
