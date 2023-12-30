#
# test_arapp
#
import sys
from typer.testing import CliRunner
import cli
from auctionresults import __app_name__, __version__

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ['--version'])
    assert result.exit_code == 0
    assert f'{__app_name__} v{__version__}' in result.stdout