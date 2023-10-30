#
# Treasuries class
#
import requests
import json
from typing import List
from Treasury import Treasury


class Treasuries:
    def get(self, cusip) -> List[Treasury]:
        response = self.load(cusip)

        if response == "":
            return []

        data = json.loads(response)

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
