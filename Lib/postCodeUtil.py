# Primary Method Functions ==================================================
# (parse by postcode)

def remPunctuation(addrString):
    newAddrString = addrString
    for index, char in enumerate(addrString):
        if char == '-' or char == '.' or char == ',':
            newAddrString = newAddrString[:index] + ' ' + newAddrString[index + 1:]
    return newAddrString

def postCodeLookup(distr, postCodeMap, cityList, cityListSimplified):
    # returns tuple (matchFound, city string)
    for districts in postCodeMap:
        if distr in districts:
            cityFromPC = remPunctuation(postCodeMap[districts].lower())
            for index, cityFromList in enumerate(cityListSimplified):
                if cityFromPC == cityFromList:
                    return True, cityList[index] # properly capitalized city
    return False, None
