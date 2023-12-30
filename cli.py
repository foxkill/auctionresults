#
# client
#

from stdnum import cusip as cu
from typing import Optional
from typing_extensions import Annotated

from prettytable import PrettyTable
from auctionresults import __app_name__, __version__, Treasuries, Treasury, TreasuryType
import typer

__vertical__ = False
# Reopening: %s\nType: %s\nIssue Date: %s\nMaturity Date: %s\nBid to Cover: %s\nPercentage bought by dealers: %s\n Interest Rate: %s\n" 

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
def latest():
    latest = Latest("") # type: ignore
    latest.get()

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

    # type = treasuryObjects[0].type
    # fields = [
    #     "Security Term", 
    #     "CUSIP",
    #     "Reopening",
    #     "Security Type", 
    #     "Issue Date", 
    #     "Maturity Date", 
    #     "Bid To Cover",
    #     "Debt purchased by dealers"]
    
    # if type == TreasuryType.BILL.value:
    #     fields.append("High Rate")
    #     fields.append("Investment Rate")
    # else:
    #     fields.append("High Yield")
    #     fields.append("Interest Rate")

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
        # bid_to_cover_ratio = treasury.getBidToCoverRatio()
        # percentage_debt_purchased_by_dealers = treasury.getPercentageDebtPurchasedByDealers()

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