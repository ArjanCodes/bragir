from click.testing import CliRunner
from bragir.__main__ import cli


def test_refuse_shorthand_logging():
    runner = CliRunner()
    result = runner.invoke(cli, ["-ll"])
    assert result.exit_code == 2


def test_refute_shorthand_logging():
    runner = CliRunner()
    result = runner.invoke(cli, ["-ll", "info"])
    assert result.exit_code == 2


def test_refute_long_logging():
    runner = CliRunner()
    result = runner.invoke(cli, ["--logging_level", "info"])
    assert result.exit_code == 2
