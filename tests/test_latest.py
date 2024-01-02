import pytest
import requests_mock

from auctionresults.treasury_type import TreasuryType
from auctionresults.latest import Latest, __auctioned_url__
from tests.latest_fixture import latest_json

__bond_url__ = 'https://www.treasurydirect.gov/TA_WS/securities/auctioned?type=Bond&days=10'

def test_latest_get(latest_json):
    latest = Latest('BOND', 10)

    with requests_mock.Mocker() as mock:
        mock.get(__auctioned_url__, json=latest_json)
        newest = latest.get()

        # 11 tresuries
        assert len(newest.root) == 11

        bills = filter(lambda x: (x.type == TreasuryType.BILL.value), newest.root)
        billsList = list(bills)

        # 0 bonds
        # 6 Bills
        assert len(billsList) == 6 

def test_lastest_url():
    latest = Latest('BOND', 10)
    url = latest.url()
    assert url == __bond_url__

def test_lastest_get_type():
    latest = Latest('bOnD', 10)
    assert latest.get_type(latest.type) == 'Bond'

def test_latest_get_days():
    latest1 = Latest('note', 10)
    assert latest1.get_days() == 10

    # Use default value 7
    latest2 = Latest('note')
    assert latest2.get_days() == 7

    # Using 0 is like using the default value
    latest3 = Latest('note', 0)
    assert latest3.get_days() == 7

def test_lastest_is_valid_type():
    latest = Latest('FrN')
    assert latest.get_type(latest.type) == 'FRN'

def test_it_should_throw_execption_if_invalid_type_is_given():
    """  
    Test that a ValueError is raised when the argument is an invalid type.
    """  
    invalidType = 'bOnDs'
    with pytest.raises(ValueError) as excinfo:  
        latest = Latest(invalidType, 8)
    assert str(excinfo.value) == f'Invalid treasury type {invalidType} given'