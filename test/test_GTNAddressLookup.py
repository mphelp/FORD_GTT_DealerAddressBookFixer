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
        actual = l.lookupCity("89aeavLONDon--", addressBook)
        self.assertEqual(actual, "London")

    def test_lookupCityDifferentCity(self):
        df = pd.DataFrame(data={'City': ['London','New Delphi'], 'Country Name': ['United Kingdom','India']})
        ai = AddressImporter()
        addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(df)

        l = GTNAddressLookup()
        actual = l.lookupCity("aev0.New.delphI.", addressBook)
        self.assertEqual("New Delphi", actual)

    def test_lookupCountry(self):
        df = pd.DataFrame(data={'City': ['London','New Delphi','Oslo'],
                                'Country Name': ['United Kingdom','India','Norway']})
        ai = AddressImporter()
        addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(df)
        l = GTNAddressLookup()
        actual = l.lookupCountry("-seNOrway", addressBook)
        self.assertEqual("New Delphi", actual)
