import xml.etree.ElementTree as ET
from typing import List
from Treasuries import Treasuries
from prettytable import PrettyTable

from TreasuryType import TreasuryType

def main():
    cusip_number = input("Enter the CUSIP number: ")

    treasuryObjects = Treasuries().get(cusip_number) 

    if len(treasuryObjects) == 0:
        print(f"Could not retrieve auction results for: {cusip_number}")
        exit(1)

    table = PrettyTable()
    table.title = treasuryObjects[0].getTerm()
    type = treasuryObjects[0].type

    fields = [
        "Security Term", 
        "CUSIP",
        "Reopening",
        "Security Type", 
        "Issue Date", "Maturity Date", 
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
    
        # print(f"Name of the security: {name} - {cusip}")
        # print(f"Percentage of debt purchased by primary dealers: {percentage_debt_purchased_by_dealers:.2f}%")
        # print(f"Bid-to-cover ratio: {bid_to_cover_ratio}")
        # print("")

    print(table)

if __name__ == '__main__':
    main()
