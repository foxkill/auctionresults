#
# Treasuries class
#
import requests
import json
from typing import List

from .treasuries_pd import TreasuriesPD
from .treasury_pd import TreasuryPD

__treasuries_url__ = 'https://www.treasurydirect.gov/TA_WS/securities/search'

class Treasuries:
    def __init__(self):
        self.treasuries = TreasuriesPD(root=[])
        self.cusip = ''

    def get(self, cusip) -> TreasuriesPD:
        if cusip == self.cusip:
            return self.treasuries

        self.cusip = cusip
        self.treasuries = TreasuriesPD(root=[])

        response = self.load(cusip)

        if response == "":
            return self.treasuries

        data = json.loads(response)

        self.treasuries = self.treasuries.model_construct(data)

        return self.treasuries

    def load(self, cusip):
        url = f'{__treasuries_url__}?cusip={cusip}&format=json'

        response = requests.get(url)

        if response.status_code == 200:
            return response.content  # type: ignore
        else:
            return ""
