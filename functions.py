# Primary Method Functions ===================================
def remComma(addrString):
    newAddrString = addrString
    for index, char in enumerate(addrString):
        if char == ',':
            newAddrString = newAddrString[:index] + ' ' + newAddrString[index + 1:]
    return newAddrString


def postCodeLookup(distr,postCodeMap):
    # returns tuple (matchFound, city string)
    for districts in postCodeMap:
        if distr in districts:
            return True, postCodeMap[districts]
    return False, None

def debugPrint(debug, key, addrElements, currentAddrIndex):
    if not debug:
        return
    print(currentAddrIndex, key + '\t: ', " ".join(addrElements))
    if key == 'noValidCity':
        print(currentAddrIndex, 'noValidCity\t: ', " ".join(addrElements))


# Method 2 dictionaries and Functions (if method 1 fails)
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

def removeDup(potentialCities):
    seen = set()
    seen_add = seen.add
    return [x for x in potentialCities if not (x in seen or seen_add(x))]

def cityStringParse(results, addrElements, currentAddrIndex, cityList, suffixes):
    matches = []
    wordCount = len(addrElements)
    for elementIndex, origWord in enumerate(addrElements):
        followingWord = ''
        #if elementIndex < wordCount and elementIndex > 0:
            # Adjust for capitalization
        word = checkAbbr(properCapitalization(origWord))
        if elementIndex < wordCount - 1:
            followingWord = properCapitalization(addrElements[elementIndex + 1])
            #followingWord = addrElements[elementIndex + 1].upper()[0] + addrElements[elementIndex + 1].lower()[1:]
        if elementIndex == len(addrElements) - 1 and len(word) > 2 and word in cityList:
            matches.append(word)
        elif len(word) > 2 and followingWord not in suffixes
            '''
            if elementIndex == len(addrElements) - 1 and len(word) > 2 and word in cityList:
                matches.append(word)
            elif len(word) > 2 and followingWord not in suffixes and word in cityList:
                matches.append(word)
            '''
    # No City found, write whitespace
    if len(matches) == 0:
        debugPrint('noValidCity', addrElements, currentAddrIndex)
        writeNoCity(results)
        return

    # Remove Duplicates and write city
    matches = removeDup(matches)
    #writeCity(results, matches[-1])
    return matches

def properCapitalization(word):
    return word.upper()[0] + word.lower()[1:]

