from myUtil import parse
from myUtil.AddressBook import AddressBook

class AddressImporter:

    def loadGTNApprovedAddressesCitiesAndCountries(self, approvedAddressesDataFrame):
        return AddressBook(approvedAddressesDataFrame[['City']].values,
                           approvedAddressesDataFrame[['Country Name']].values)
