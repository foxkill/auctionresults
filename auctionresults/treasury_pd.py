#
# Defines a treasury object (bill, frn, tip, note, bond) via pedantic
#
from typing import Any
from pydantic import BaseModel, Json

class TreasuryPD(BaseModel):
    cusip: str


