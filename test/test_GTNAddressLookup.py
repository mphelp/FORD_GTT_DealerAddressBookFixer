import pandas as pd
from unittest import TestCase

from myUtil.AddressImporter import AddressImporter
from myUtil.GTNAddressLookup import GTNAddressLookup

class TestGTNAddressLookup(TestCase):
    def test_lookupCity(self):
        df = pd.DataFrame(data={'City': ['London'], 'Country Name': ['United Kingdom']})
        ai = AddressImporter()
        addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(df)

        l = GTNAddressLookup()
        actualCity = l.lookupCity("89aeavLONDon--", addressBook)
        self.assertEqual(actualCity, "London")
