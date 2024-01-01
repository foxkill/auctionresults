#
# client
#

from stdnum import cusip as cu
from typing import Optional
from typing_extensions import Annotated

from prettytable import PrettyTable
from auctionresults import __app_name__, __version__, Treasuries, Treasury, TreasuryType, Latest
import typer

__vertical__ = False

app = typer.Typer(help=__app_name__)

def version(value: bool) -> None:
    if value:
        typer.echo(__app_name__ + ' v' + __version__)
        raise typer.Exit()

def vertical(value: bool):
    global __vertical__
    if value:
        __vertical__ = True
    else:
        __vertical__ = False

@app.command()
def latest(
    type: Annotated[Optional[str], typer.Option(help='Type of the treasury to quey (Bill, Note, Bond, FRN, CMB)')] = '',
    days: Annotated[Optional[int], typer.Option(help='The number of days to look back - default is 7')] = 0
):
    if type is None:
        type = ''
    
    if days is None:
        days = 0

    latest = Latest(type, days)
    treasuries = latest.get()
    for treasury in treasuries:
        print(treasury)
        print('')

# vertical: Annotated[bool, typer.Option(help='Print the output of a query (rows) vertically.')] = False):
# 912828YF1
@app.command()
def get(cusip: Annotated[Optional[str], typer.Argument()] = None):
    if cusip is None:
        cusip_number = input("Enter the CUSIP number: ")
    else:
        cusip_number = cusip

    if not cu.is_valid(cusip_number):
        print("Invalid cusip number given.")
        exit (1)

    cusip_number = cusip_number.strip()
    treasuryObjects = Treasuries().get(cusip_number) 

    if len(treasuryObjects) == 0:
        print(f"Could not retrieve auction results for: {cusip_number}")
        exit(1)

    if __vertical__ == True:
        for treasury in treasuryObjects:
            print(treasury)
        return

    table = PrettyTable()
    table.title = treasuryObjects[0].getTerm()
    fields = treasuryObjects[0].get_fields()

    table.field_names = fields

    table.align["Security Term"] = "l"
    table.align["Security Type"] = "l"
    table.align["Bid To Cover"] = "r"
    table.align["Debt purchased by dealers"] = "r"

    if type == TreasuryType.BILL.value:
        table.align["High Rate"] = "r"
        table.align["Investment Rate"] = "r"
    else:
        table.align["High Yield"] = "r"
        table.align["Interest Rate"] = "r"

    for treasury in treasuryObjects:
        if type == TreasuryType.BILL.value:
            yld = "%.3f%%" % treasury.highDiscountRate
            rate = "%.3f%%" % treasury.highInvestmentRate
        else:
            yld = "%.3f%%" % treasury.highYield 
            rate = "%.3f%%" % treasury.interestRate

        table.add_row([
            treasury.securityTerm, 
            treasury.cusip, 
            "Yes" if treasury.reopening == True else "No",
            treasury.type,
            treasury.issueDate, 
            treasury.maturityDate, 
            "%.2f" % treasury.getBidToCoverRatio(),
            "%.2f%%" % treasury.getPercentageDebtPurchasedByDealers(),
            yld, 
            rate])
 
        typer.echo(table)

@app.callback()
def main(
    vertical: Optional[bool] = typer.Option(
        None, 
        "--vertical", 
        "-E", 
        help="Prints the output in verital format", 
        callback=vertical, 
        is_eager=True
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show application version and exit",
        callback=version,
        is_eager=True
    ),
) -> None:
    return