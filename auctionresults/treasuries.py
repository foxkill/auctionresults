#
# Treasuries class
#
import requests
import json
from typing import List
from auctionresults.treasury import Treasury

class Treasuries:
    def __init__(self):
        self.treasuries = []
        self.cusip = ''

    def get(self, cusip) -> List[Treasury]:
        if cusip == self.cusip:
            return self.treasuries

        self.cusip = cusip
        self.treasuries = []

        response = self.load(cusip)

        if response == "":
            return self.treasuries

        data = json.loads(response)

        self.treasuries = self.to_objects(cusip, data)

        return self.treasuries

    def to_objects(self, cusip, data):
        treasuries = []
        for treasury in data:
            t = Treasury()

            t.cusip = cusip
            t.highDiscountRate = treasury["highDiscountRate"]
            t.highInvestmentRate = treasury["highInvestmentRate"]
            t.interestRate = treasury["interestRate"]
            t.highYield = treasury["highYield"]
            t.reopening = treasury["reopening"]
            t.issueDate = treasury["issueDate"]
            t.maturityDate = treasury["maturityDate"]
            t.totalAccepted = treasury["totalAccepted"]
            t.term = treasury["term"]
            t.type = treasury["type"]
            t.securityTerm = treasury["securityTerm"]
            t.primaryDealerAccepted = treasury["primaryDealerAccepted"]
            t.bidToCoverRatio = treasury["bidToCoverRatio"]

            treasuries.append(t)

        return treasuries

    def load(self, cusip):
        url = f"https://www.treasurydirect.gov/TA_WS/"
        api = f"securities/search?cusip={cusip}&format=json"

        response = requests.get(url + api)

        if response.status_code == 200:
            return response.content  # type: ignore
        else:
            return ""
