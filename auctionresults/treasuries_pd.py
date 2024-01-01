#
# TreasuriesPD
#
from typing import List
from pydantic import RootModel
from .treasury_pd import TreasuryPD

class TreasuriesPD(RootModel):
    root: List[TreasuryPD]