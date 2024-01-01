#
# Defines a treasury object (bill, frn, tip, note, bond) via pedantic
#
from copy import copy
from datetime import date, datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator
from .treasury_type import TreasuryType

__fmt_str__ = '%s:\t%s %%s'

__fields__ = [
    "Security Term", 
    "CUSIP",
    "Reopening",
    "Security Type", 
    "Issue Date", 
    "Maturity Date", 
    "Bid To Cover",
    "Dealers"
]

StrFloat = Annotated[float, BeforeValidator(lambda v: float(v) if len(v) != 0 else 0)]

# from numbers import Number
# from typing import Any

# from pydantic import BaseModel, validator
# from pydantic.fields import ModelField

# class Foo(BaseModel):
#     a: int
#     b: float
#     c: complex
#     d: list[float]
#     e: str

#     @validator("*", pre=True, each_item=True)
#     def empty_to_zero(cls, v: Any, field: ModelField) -> Any:
#         if issubclass(field.type_, Number) and v == "":
#             return field.type_(0)
#         return v

#     class Config:
#         arbitrary_types_allowed = True  # only needed for `complex`

# if __name__ == "__main__":
#     data = {
#         "a": "",
#         "b": "",
#         "c": "",
#         "d": ["3.14", ""],
#         "e": "Hi mom",
#     }
#     foo = Foo.parse_obj(data)
#     print(foo)
#     print(foo.dict())
class TreasuryPD(BaseModel):
    cusip: str
    type: str
    reopening: bool
    highDiscountRate: StrFloat
    highInvestmentRate: StrFloat
    highYield: StrFloat
    interestRate: StrFloat
    securityTerm: str
    issueDate: datetime
    maturityDate: datetime

    def get_fields(self):
        fields = copy(__fields__)

        if self.type == TreasuryType.BILL.value:
            fields.append("High Rate")
            fields.append("Investment Rate")
        else:
            fields.append("High Yield")
            fields.append("Interest Rate")
    
        return fields

    def __str__(self):
        yld = ''
        rate = ''

        if self.type == TreasuryType.BILL.value:
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
            self.issueDateAsStr, 
            self.maturityDateAsStr,
            "%.2f" % self.getBidToCoverRatio(),
            "%.2f%%" % self.getPercentageDebtPurchasedByDealers(),
            yld, 
            rate
        )

    @property
    def issueDateAsStr(self) -> str:
        return self.issueDate.strftime('%m/%d/%Y')

    @property
    def maturityDateAsStr(self) -> str:
        return self.maturityDate.strftime('%m/%d/%Y')

    def getBidToCoverRatio(self):
        return 0.0
    
    def getPercentageDebtPurchasedByDealers(self):
        return .0