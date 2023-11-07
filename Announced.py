#
# Get the currently announced auctions
#

class Announced:
    """docstring for Announced."""
    def __init__(self, arg):
        self.arg = arg
        return

    def get(self):
        # https://www.treasurydirect.gov/TA_WS/securities/announced?format=html&type=FRN
        return