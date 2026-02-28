"""Unit tests for CLI commands."""

from typer.testing import CliRunner

from citysense.cli.main import app

runner = CliRunner()


def test_cli_pilot_status() -> None:
    """Test pilot status command."""
    result = runner.invoke(app, ["pilot", "status"])
    assert result.exit_code == 0
    assert "Pilot" in result.output or "not set" in result.output
