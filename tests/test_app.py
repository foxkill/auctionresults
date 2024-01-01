#
# test_arapp
#
import pytest
import requests_mock
from typer.testing import CliRunner
import cli
from auctionresults import __app_name__, __version__
from auctionresults.latest import __url__
from auctionresults.treasuries import __treasuries_url__
from .latest_fixture import latest_json
from .get_fixture import get_json

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0
    assert f'{__app_name__} v{__version__}' in result.stdout

def test_help():
    result = runner.invoke(cli.app, ['--help'])
    assert result.exit_code == 0
    assert '-E, --vertical' in result.stdout

def test_lastest(latest_json):
    with requests_mock.Mocker() as mock:
        mock.get(__url__, json=latest_json)
        result = runner.invoke(cli.app, ['latest', '--type', 'bond', '--days', '60'])
        assert result.exit_code == 0

def test_get(get_json):
    with requests_mock.Mocker() as mock:
        mock.get(__treasuries_url__, json=get_json)
        result = runner.invoke(cli.app, ['get', '912828YF1'])
        assert result.exit_code == 0
