class Address:
    def __init__(self, city, countryName, add1, add2, postalCode, locationName):
        self.city = city
        self.countryName = countryName
        self.add1 = add1
        self.add2 = add2
        self.postalCode = postalCode
        self.locationName = locationName

    def __repr__(self):
        print('City: {}, Country Name: {}, Add1: {}, Add2: {}, Postal Code: {}'.format(
            self.city, self.countryName, self.add1, self.add2, self.postalCode
        ))
