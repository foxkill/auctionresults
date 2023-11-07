#
# Get the currently announced auctions
#

class Announced:
    URL = f"https://www.treasurydirect.gov/TA_WS/securities/announced?format=html&type={type}"
    """docstring for Announced."""
    def __init__(self, arg):
        self.arg = arg
        return

    def get(self, type):
        url = self.URL
        return