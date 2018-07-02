import pandas as pd
from myUtil import parse
class GTNAddressLookup:

    def __init__(self, approvedAddressesFile='Please specify file path', approvedSheetName='Specify sheet'):
        self.approvedAddressesFile=approvedAddressesFile
        self.approvedSheetName = approvedSheetName

    def loadGTNApprovedAddressesCitiesAndCountries(self):
        self.approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(self.approvedAddressesFile),
                                                   self.approvedSheetName)
        #for i in self.approvedAddressesDataFrame:
            #print(f'{i}')
        #self.approvedCountries = [parse.convertToStr(getattr(addr, 'Country Name')) for addr in
                                #  approvedAddressesDataFrame[['Country Name']].itertuples()]
        #self.approvedCountries = [type(country) for country in
                                  #self.approvedAddressesDataFrame[['Country Name']].tolist()]
        #print(self.approvedCountries)
        #print('Andorra' in self.approvedCountries)
       # self.approvedCities    = [parse.convertToStr(getattr(addr, 'City')) for addr in
                        #          self.approvedAddressesDataFrame[['City']].itertuples()]

  #  self.approvedCitiesSimple = [parse.remPunctuation(city.lower()) for city in self.approvedCities]
      #  self.approvedCountriesSimple = [parse.remPunctuation(country.lower()) for country in self.approvedCountries]

    def cityFoundViaLookup(self, addr, cityList, cityListSimplified):
        addrSimplified = parse.remPunctuation(addr.lower())
        matchesList = [cityList[index] for index, citySimple in enumerate(cityListSimplified) if
                       citySimple in addrSimplified and len(citySimple) >= 4]
        if len(matchesList) == 0:
            return None
        else:
            return max(matchesList, key=len)