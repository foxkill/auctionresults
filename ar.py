import xml.etree.ElementTree as ET
from typing import List
from Treasuries import Treasuries
from prettytable import PrettyTable

def main():
    cusip_number = input("Enter the CUSIP number: ")

    treasuryObjects = Treasuries().get(cusip_number) 

    table = PrettyTable()
    table.title = treasuryObjects[0].getTerm()
    table.field_names = [
        "Security Term", 
        "CUSIP",
        "Reopening",
        "Security Type", 
        "Issue Date", "Maturity Date", 
        "Bid To Cover",
        "Debt purchased by dealers",
        "High Yield", "Interest Rate"]

    for treasury in treasuryObjects:
        # bid_to_cover_ratio = treasury.getBidToCoverRatio()
        # percentage_debt_purchased_by_dealers = treasury.getPercentageDebtPurchasedByDealers()

        table.add_row([
            treasury.securityTerm, 
            treasury.cusip, 
            "Yes" if treasury.reopening == True else "No",
            treasury.term,
            treasury.issueDate, 
            treasury.maturityDate, 
            "%.2f" % treasury.getBidToCoverRatio(),
            "%.2f%%" % treasury.getPercentageDebtPurchasedByDealers(),
            "%.3f%%" % treasury.highYield, 
            "%.3f%%" % treasury.interestRate])
    
        # print(f"Name of the security: {name} - {cusip}")
        # print(f"Percentage of debt purchased by primary dealers: {percentage_debt_purchased_by_dealers:.2f}%")
        # print(f"Bid-to-cover ratio: {bid_to_cover_ratio}")
        # print("")

    print(table)

if __name__ == '__main__':
    main()
