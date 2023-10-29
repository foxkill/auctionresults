#
# Treasury Object
#
import requests
import datetime
import xml.etree.ElementTree as ET

class Treasury:
    def __init__(self):
        self._cusip = ""
        self._type = ""
        self._term = ""
        self._securityTerm = ""
        self._reopening = False
        self._issueDate = datetime.date.today()
        self._maturityDate = datetime.date.today()
        self._highYield = .0
        self._interestRate = .0
        self.hasResults = False

        # self.xmlFilenameCompetitiveResults = xmlFilenameCompetitiveResults
        # self.term = term
        # self.reopening = True if reopening == "Yes" else False
        # set afterwards
        # self.percentageDebtPurchasedByDealers = .0
        # self._bidToCoverRatio = .0
        # self._primaryDealerAccepted = .0
        # self._totalAccepted = .0
    
    @property
    def cusip(self) -> str:
        return self._cusip
    
    @cusip.setter
    def cusip(self, value):
        self._cusip = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def term(self) -> str:
        return self._term
    
    @term.setter
    def term(self, value):
        self._term = value

    @property
    def securityTerm(self) -> str:
        return self._securityTerm

    @securityTerm.setter
    def securityTerm(self, value):
        self._securityTerm = value

    @property
    def reopening(self) -> bool:
        return self._reopening

    @reopening.setter
    def reopening(self, value):
        self._reopening = True if value == "Yes" else False

    @property 
    def issueDate(self):
        return self._issueDate.strftime("%m/%d/%Y")

    @issueDate.setter
    def issueDate(self, value: str):
        self._issueDate = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

    @property
    def maturityDate(self) -> str:
        return self._maturityDate.strftime("%m/%d/%Y")
    
    @maturityDate.setter
    def maturityDate(self, value: str):
        self._maturityDate = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    
    @property
    def highYield(self) -> float:
        return self._highYield

    @highYield.setter
    def highYield(self, value: str):
        self._highYield = float(value)

    @property
    def interestRate(self) -> float:
        return self._interestRate

    @interestRate.setter
    def interestRate(self, value):
        self._interestRate = float(value)

    @property
    def bidToCoverRatio(self) -> float:
        return self._bidToCoverRatio

    @bidToCoverRatio.setter
    def bidToCoverRatio(self, value: str):
        self._bidToCoverRatio = float(value)

    @property
    def primaryDealerAccepted(self) -> float:
        return self._primaryDealerAccepted 

    @primaryDealerAccepted.setter
    def primaryDealerAccepted(self, value: str):
        self._primaryDealerAccepted = float(value)

    @property
    def totalAccepted(self) -> float:
        return self._totalAccepted
    
    @totalAccepted.setter
    def totalAccepted(self, value: str):
        self._totalAccepted = float(value)

    def calculate_auction_results(self):
        if self.hasResults == True:
            return None

        self.percentageDebtPurchasedByDealers = (self.primaryDealerAccepted / self.totalAccepted) * 100
        self.hasResults = True
        return None
        ###
        # xml_data = self.download_auction_result()
        # if xml_data == "":
        #     return None

        # root = ET.fromstring(xml_data)
        # results = root.find('AuctionResults')
        # if results == None:
        #     return None

        # total_debt = float(results.find('TotalAccepted').text) # type: ignore
        # total_dealer_purchases = float(results.find('PrimaryDealerAccepted').text) # type: ignore

        # self.percentageDebtPurchasedByDealers = (total_dealer_purchases / total_debt) * 100
        # self.bidToCoverRatio =float(results.find('BidToCoverRatio').text)  # type: ignore

        # self.hasResults = True

    def download_auction_result(self) -> str:
        if self.hasResults == True:
            return ""

        filename = self.xmlFilenameCompetitiveResults
        response = requests.get(f"https://www.treasurydirect.gov/xml/{filename}")
        if response.status_code == 200:
            return response.content # type: ignore
        else:
            return ""
        
    def getBidToCoverRatio(self):
        self.calculate_auction_results()
        return self.bidToCoverRatio
    
    def getPercentageDebtPurchasedByDealers(self) -> float:
        self.calculate_auction_results()
        return self.percentageDebtPurchasedByDealers

    def getTerm(self) -> str:
        return self.term + " " + self.type

    def getName(self) -> str:
        return self.term + " " + self.type

    def getCusip(self) -> str:
        return self.cusip