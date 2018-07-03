from myUtil import parse


class AddressBook:
    def __init__(self, _approvedCities, _approvedCountries):
        self.approvedCities = _approvedCities
        self.approvedCountries = _approvedCountries
        self.approvedCitiesSimple = [parse.remPunctuation(c[0].lower()) for c
                               in self.approvedCities]
        self.approvedCountriesSimple = [parse.remPunctuation(c[0].lower()) for c
                                  in self.approvedCountries]
