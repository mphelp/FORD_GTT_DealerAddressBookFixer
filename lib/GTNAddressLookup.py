import pandas as pd
from lib import parse
class GTNAddressLookup:

    def __init__(self, approvedAddressesFile='dependencies/GTNexus_CityList_20180208.xlsx'):
        self.approvedAddressesFile=approvedAddressesFile

    def loadGTNApprovedAddresses(self):
        self.approvedAddressesDataFrame = pd.read_excel(self.approvedAddressesFile)

    def selectKeyColumnsFromDataFrame(self):
        self.approvedCities    = [parse.convertToStr(getattr(addr, 'City')) for addr in
                                  self.approvedAddressesDataFrame[['City']].itertuples()]
        self.approvedCountries = [parse.convertToStr(getattr(addr, 'Country Name')) for addr in
                                  self.approvedAddressesDataFrame[['Country Name']].itertuples()]