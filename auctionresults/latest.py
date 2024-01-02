#
# Retrieves the latest auctions.
#
import json
import requests
from typing import List

from .treasury_type import TreasuryType
from .treasuries_pd import TreasuriesPD

__auctioned_url__ = 'https://www.treasurydirect.gov/TA_WS/securities/auctioned'

class Latest:
	"""docstring for Latest."""
	def __init__(self, type: str, days: int = 7):
		self.type = type if type != "" else ""

		if self.type != "":
			if self.is_valid_type(self.type) == False:
				raise ValueError(f'Invalid treasury type {self.type} given')

		self.days = 7 if days <= 0 else days
		self.treasuries = []

	def get(self) -> TreasuriesPD:
		self.treasuries = []

		response = self.load()
		if response == '':
			return TreasuriesPD(root=[])
		
		data = json.loads(response)

		return TreasuriesPD(root=data)

	def url(self) -> str:
		url = __auctioned_url__

		if self.type != '':
			url += ('?type=' + self.get_type(self.type) + '&days=' + str(self.days))
		else:
			url += ('?days=' + str(self.days))

		return url

	def get_type(self, value: str) -> str:
		check = value.lower().title()

		if check in ['Frn', 'Cmb']:
			return check.upper()

		return check

	def get_days(self) -> int:
		return self.days

	def is_valid_type(self, type: str) -> bool:
		mytype = self.get_type(type)
		try:
			TreasuryType(mytype)
			return True
		except Exception as e:
			return False
	
	def load(self):
		response = requests.get(self.url())
		return response.content if response.status_code == 200 else ""