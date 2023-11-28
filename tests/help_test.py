from click.testing import CliRunner
from bragir.__main__ import cli


def test_shorthand_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["-h"])
    assert result.exit_code == 0


def test_long_help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
