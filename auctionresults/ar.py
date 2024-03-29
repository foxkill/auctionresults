import xml.etree.ElementTree as ET
from typing import List, Optional

import typer
from prettytable import PrettyTable
from stdnum import cusip as cu
from typing_extensions import Annotated

from auctionresults.latest import Latest
from auctionresults.treasuries import Treasuries
from auctionresults.treasury_type import TreasuryType


# 912828YF1
def get(cusip: Annotated[Optional[str], typer.Argument()] = None, 
        vertical: Annotated[bool, typer.Option(help='Print the output of a query (rows) vertically.')] = False):
    if cusip is None:
        cusip_number = input("Enter the CUSIP number: ")
    else:
        cusip_number = cusip

    if not cu.is_valid(cusip_number):
        print("Invalid cusip number given.")
        exit (1)

    cusip_number = cusip_number.strip()
    treasuryObjects = Treasuries().get(cusip_number) 

    if len(treasuryObjects.root) == 0:
        print(f"Could not retrieve auction results for: {cusip_number}")
        exit(1)
    
    table = PrettyTable()
    table.title = treasuryObjects.root[0].term_as_str
    type = treasuryObjects.root[0].type

    fields = [
        "Security Term", 
        "CUSIP",
        "Reopening",
        "Security Type", 
        "Issue Date", 
        "Maturity Date", 
        "Bid To Cover",
        "Debt purchased by dealers"]
    
    if type == TreasuryType.BILL.value:
        fields.append("High Rate")
        fields.append("Investment Rate")
    else:
        fields.append("High Yield")
        fields.append("Interest Rate")

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

    for treasury in treasuryObjects.root:
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
    
        # print(f"Name of the security: {name} - {cusip}")
        # print(f"Percentage of debt purchased by primary dealers: {percentage_debt_purchased_by_dealers:.2f}%")
        # print(f"Bid-to-cover ratio: {bid_to_cover_ratio}")
        # print("")

    print(table)