import pandas as pd
class GTNAddressLookup:

    def __init__(self, approvedAddressesFile='dependencies/GTNexus_CityList_20180208.xlsx'):
        self.approvedAddressesFile=approvedAddressesFile

    def loadGTNApprovedAddresses(self):
        self.approvedAddressesDataFrame = pd.read_excel(self.approvedAddressesFile)

    def selectKeyColumnsFromDataFrame(self):
        self.approvedCities    =
        self.approvedCountries =