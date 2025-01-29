import pytest
from click.testing import CliRunner
from bragir.__main__ import cli


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_shorthand_help(cli_runner: CliRunner):
    result = cli_runner.invoke(cli, ["-h"])
    assert result.exit_code == 0


def test_long_help(cli_runner: CliRunner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
