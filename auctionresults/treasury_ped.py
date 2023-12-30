#
# Defines a treasury object (bill, frn, tip, note, bond) via pedantic
#
from pydantic import BaseModel

class TreasuryPed(BaseModel):
    pass


# t = TreasuryPed()
# t.parse_raw("{}")
    
