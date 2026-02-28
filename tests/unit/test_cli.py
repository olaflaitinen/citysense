"""Unit tests for CLI."""

from typer.testing import CliRunner

from citysense.cli.main import app

runner = CliRunner()


def test_cli_app_exists() -> None:
    """Test CLI app is defined."""
    assert app is not None


def test_cli_help() -> None:
    """Test CLI help."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "citysense" in result.output.lower() or "Usage" in result.output


def test_cli_pilot_help() -> None:
    """Test pilot command help."""
    result = runner.invoke(app, ["pilot", "--help"])
    assert result.exit_code == 0


def test_cli_query_help() -> None:
    """Test query command help."""
    result = runner.invoke(app, ["query", "--help"])
    assert result.exit_code == 0
