# Primary and Secondary Method Functions + Maps ==================================================
# (parse by postcode)

def convertToStr(addr):
    if not isinstance(addr, str):
        return ''
    else:
        return addr

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

abbrMap = {
    "M'well": 'Motherwell',
    'Northants': 'Northamptonshire',
    'Berwick': 'Berwick-upon-Tweed',
    'Holme-on-spalding': 'Holme-on-Spalding-Moor',
    'Holy': 'Holytown',
    'Spald': 'Holme-on-Spalding-Moor',
    'Soton': 'Southampton',
    'Glas': 'Glasgow',
    'Eastleig': 'Eastleigh',
    'Doncs': 'Doncaster',
    'Billinigham': 'Billingham',
    'Lcester': 'Leicester',
    'Doncaste': 'Doncaster',
}

def checkAbbr(word):  # check list of exceptions/abbreviations
    if word in abbrMap:
        return abbrMap[word]
    return word

def cityStringParse(addr, cityList, cityListSimplified):
    matchesList = []
    addrSimplified = remPunctuation(addr.lower())
    #for index, citySimple in enumerate(cityListSimplified):
        #if citySimple in addrSimplified:
            #matchesList.append(cityList[index])
    # Alternative:
    matchesList = [cityList[index] for index, citySimple in enumerate(cityListSimplified) if
                   citySimple in addrSimplified]

    if len(matchesList) == 0:
        return False, None
    else:
        return True, max(matchesList, key=len)

