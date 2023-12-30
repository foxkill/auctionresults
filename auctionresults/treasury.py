#
# Treasury Object
#
import requests
import datetime
import xml.etree.ElementTree as ET

from .treasurytype import TreasuryType

__get_url__ = 'https://www.treasurydirect.gov/xml/'
__fmt_str__ = '%s:\t%s %%s'

# __header__ = "Type: %s\nCusip: %s\nReopening: %s\nType: %s\nIssue Date: %s\nMaturity Date: %s\nBid to Cover: %s\n"
__fields__ = [
        "Security Term", 
        "CUSIP",
        "Reopening",
        "Security Type", 
        "Issue Date", 
        "Maturity Date", 
        "Bid To Cover",
        "Dealers"]

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
        self._highDiscountRate = .0
        self._highInvestmentRate = .0
        self.hasResults = False

        self.xmlFilenameCompetitiveResults = ""
        self._primaryDealerAccepted = .0
        self._bidToCoverRatio = .0
        self._totalAccepted = .0
        # self.term = term
        # self.reopening = True if reopening == "Yes" else False
        # set afterwards
        # self.percentageDebtPurchasedByDealers = .0
    
    def get_fields(self):
        fields = __fields__

        if type == TreasuryType.BILL.value:
            fields.append("High Rate")
            fields.append("Investment Rate")
        else:
            fields.append("High Yield")
            fields.append("Interest Rate")
    
        return fields

    def __str__(self):
        yld = ''
        rate = ''

        if self.type == TreasuryType.BILL.name:
            yld = '%.3f%%' % self.highDiscountRate
            rate = '%.3f%%' % self.highInvestmentRate
        else:
            yld = '%.3f%%' % self.highYield 
            rate = '%.3f%%' % self.interestRate

        fmtstr = '\n'.join([__fmt_str__ % ((i, '\t') if i == 'CUSIP' else (i, '')) for i in self.get_fields()])
        
        return fmtstr % (self.securityTerm, 
            self.cusip, 
            'Yes' if self.reopening == True else 'No',
            self.type,
            self.issueDate, 
            self.maturityDate,
            "%.2f" % self.getBidToCoverRatio(),
            "%.2f%%" % self.getPercentageDebtPurchasedByDealers(),
            yld, 
            rate
        )

    @property
    def highDiscountRate(self) -> float:
        return self._highDiscountRate
    
    @highDiscountRate.setter
    def highDiscountRate(self, value: str):
        try:
            self._highDiscountRate = float(value)
        except:
            self._highDiscountRate = 0
    
    @property
    def highInvestmentRate(self) -> float:
        return self._highInvestmentRate

    @highInvestmentRate.setter
    def highInvestmentRate(self, value: str):
        try:
            self._highInvestmentRate = float(value)
        except:
            self._highInvestmentRate = 0

        
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
        self._reopening = True if value == 'Yes' else False

    @property 
    def issueDate(self):
        return self._issueDate.strftime('%m/%d/%Y')

    @issueDate.setter
    def issueDate(self, value: str):
        self._issueDate = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

    @property
    def maturityDate(self) -> str:
        return self._maturityDate.strftime('%m/%d/%Y')
    
    @maturityDate.setter
    def maturityDate(self, value: str):
        self._maturityDate = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
    
    @property
    def highYield(self) -> float:
        return self._highYield

    @highYield.setter
    def highYield(self, value: str):
        try:
            self._highYield = float(value)
        except:
            self._highYield = .0

    @property
    def interestRate(self) -> float:
        return self._interestRate

    @interestRate.setter
    def interestRate(self, value: str):
        if value == '':
            self._interestRate = .0
            return
        self._interestRate = float(value)

    @property
    def bidToCoverRatio(self) -> float:
        return self._bidToCoverRatio

    @bidToCoverRatio.setter
    def bidToCoverRatio(self, value: str):
        try:
            self._bidToCoverRatio = float(value)
        except:
            self._bidToCoverRatio = 0

    @property
    def primaryDealerAccepted(self) -> float:
        return self._primaryDealerAccepted

    @primaryDealerAccepted.setter
    def primaryDealerAccepted(self, value: str):
        try:
            self._primaryDealerAccepted = float(value)
        except:
            self._primaryDealerAccepted = 0

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

    def download_auction_result(self) -> str:
        if self.hasResults == True:
            return ''

        filename = self.xmlFilenameCompetitiveResults
        response = requests.get(f'https://www.treasurydirect.gov/xml/{filename}')
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