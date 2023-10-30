#
# Treasury Type
#
from enum import Enum

class TreasuryType(Enum):
    """The different types of treasuries"""
    BILL = "Bill"
    NOTE = "Note"
    BOND = "Bond"

    