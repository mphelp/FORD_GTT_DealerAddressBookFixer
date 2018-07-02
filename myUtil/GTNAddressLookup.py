import pandas as pd
from myUtil import parse
class GTNAddressLookup:

    def __init__(self, approvedAddressesFile='Please specify file path'):
        self.approvedAddressesFile=approvedAddressesFile

    def loadGTNApprovedAddressesCitiesAndCountries(self):
        approvedAddressesDataFrame = pd.read_excel(self.approvedAddressesFile)
        self.approvedCities    = [parse.convertToStr(getattr(addr, 'City')) for addr in
                                  approvedAddressesDataFrame[['City']].itertuples()]
        self.approvedCountries = set(parse.convertToStr(getattr(addr, 'Country Name')) for addr in
                                  approvedAddressesDataFrame[['Country Name']].itertuples())
        self.approvedCitiesSimple = [parse.remPunctuation(city.lower()) for city in self.approvedCities]
        self.approvedCountriesSimple = [parse.remPunctuation(country.lower()) for country in self.approvedCountries]

    def cityFoundViaLookup(self, addr, cityList, cityListSimplified):
        addrSimplified = parse.remPunctuation(addr.lower())
        matchesList = [cityList[index] for index, citySimple in enumerate(cityListSimplified) if
                       citySimple in addrSimplified and len(citySimple) >= 4]
        if len(matchesList) == 0:
            return None
        else:
            return max(matchesList, key=len)