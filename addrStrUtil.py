# Seconday method dictionaries and Functions (if method 1 fails) ===============
# (parse by entire address string)

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
    addrLower = addr.lower()
    for index, citySimple in enumerate(cityListSimplified):
        if citySimple in addrLower:
            matchesList.append(cityList[index])
    if len(matchesList) == 0:
        return False, None
    else:
        return True, max(matchesList, key=len)
