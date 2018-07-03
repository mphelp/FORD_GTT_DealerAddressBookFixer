import pandas as pd
import numpy as np
from myUtil import parse
class GTNAddressLookup:

    def __init__(self, approvedAddressesFile='Please specify file path', approvedSheetName='Specify sheet'):
        self.approvedAddressesFile=approvedAddressesFile
        self.approvedSheetName = approvedSheetName

    def loadGTNApprovedAddressesCitiesAndCountries(self):
        approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(self.approvedAddressesFile),
                                                   self.approvedSheetName)

        self.approvedCities = approvedAddressesDataFrame[['City']].values
        self.approvedCountries = approvedAddressesDataFrame[['Country Name']].values
        self.approvedCitiesSimple = [parse.remPunctuation(c[0].lower()) for c
                                     in self.approvedCities]
        self.approvedCountriesSimple = [parse.remPunctuation(c[0].lower()) for c
                                        in self.approvedCountries]



        # Quick tests ...

        #print(self.approvedCities[2])
        #print(self.approvedCitiesSimple[2])
        #print('Encamp is in approved cities : {}'.format('Encamp' in self.approvedCities))
        #print('encamp is in simple approved : {}'.format('encamp' in self.approvedCitiesSimple))

        #cityMatchesList = [self.approvedCities[index].item(0) for index, citySimple in
                           #enumerate(self.approvedCitiesSimple) if
                           #citySimple in 'stratford upon avon' and len(citySimple) >= 3]
        #print(cityMatchesList)
        #print('Len: {}'.format(len(cityMatchesList)))
        #returnWord = max(cityMatchesList, key=len)
        #print('Returns: {}'.format(returnWord))
        #print('Return type: {}'.format(type(returnWord)))
        #print(returnWord.item(0))

        # print('Type: {}'.format(type(returnWord.item(0))))

        ### Debugging Purposes:
        #print(self.approvedCitiesSimple)
        #print('{}'.format('New York' in self.approvedCities))
        #print('Gabon' in self.approvedCountries)
        #self.approvedCitiesSimple = np.ndarray([parse.remPunctuation(c.lower() for c in
                                                #self.approvedCities)])
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

    def cityFoundViaLookup(self, addr):
        addrSimplified = parse.remPunctuation(addr.lower())
        matchesList = [self.approvedCities[index].item(0) for index, citySimple in
                       enumerate(self.approvedCitiesSimple) if
                       citySimple in addrSimplified and len(citySimple) >= 3]
        if len(matchesList) == 0:
            return None
        else:
            return max(matchesList, key=len)