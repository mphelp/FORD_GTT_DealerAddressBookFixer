from myUtil import parse

class GTNAddressLookup:
    """This class contains the central algrorithms for address parsing."""

    # Lookup city default method: search for a match between
    # source address line string and entry in GTN approved city/country address book
    def lookupCity(self, addr, addressBook):
        if not isinstance(addr, str):
            return None
        addrSimplified = parse.remPunctuation(addr.lower())
        matchesList = [addressBook.approvedCities[index].item(0) for index, citySimple in
                       enumerate(addressBook.approvedCitiesSimple) if
                       citySimple in addrSimplified and len(citySimple) >= 3]
        if len(matchesList) == 0:
            return None
        else:
            return max(matchesList, key=len)