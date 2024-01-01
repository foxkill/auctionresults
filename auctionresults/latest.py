#
# Retrieves the latest auctions.
#
import json
import requests
from typing import List

from .treasuries_pd import TreasuryPD
from .treasuries_pd import TreasuriesPD

__url__ = 'https://www.treasurydirect.gov/TA_WS/securities/auctioned'

class Latest:
	"""docstring for Latest."""
	def __init__(self, type: str, days: int = 7):
		self.type = type if type != "" else ""
		self.days = 7 if days == 0 else days
		self.treasuries = []

	def get(self) -> List[TreasuryPD]:
		self.treasuries = []
		response = self.load()
		if response == '':
			return []
		
		data = json.loads(response)
		t = TreasuriesPD(root=data)
		return t.root

	def load(self):
		url = __url__

		if self.type != '':
			url += ('?type=' + self.type.lower().title() + '&days=' + str(self.days))
		else:
			url += ('?days=' + str(self.days))

		response = requests.get(url)

		return response.content if response.status_code == 200 else ""