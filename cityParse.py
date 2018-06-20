### Author: Matthew Phelps, Updated: June 19 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company


# Variables
badAddress = 0  # valid addresses
goodAddress = 0  # invalid addresses
addressCount = 4  # for debugging, 5 is first index of column
debug = True  # examine invalid addresses
cityListTextFile = 'GTNcityList.txt'

# Primary Method Functions ===================================
def remCommaPeriods(addrString):
    for index, char in enumerate(addrString):
        if char == ',' or char == '.':
            addrString = addrString[:index] + ' ' + addrString[index + 1:]
    return addrString

def writeNoCity(FILE):
    incrBadAddress()
    FILE.write('\n')

def writeCityFromDistricts(FILE, districts):
    incrGoodAddress()
    FILE.write(postCodeDistrictMap[districts] + '\n')

def writeCity(FILE, city):  # new function
    incrGoodAddress()
    FILE.write(city + '\n')

def districtFound(distr):
    # returns tuple (matchFound, districts key string)
    for districts in postCodeDistrictMap:
        if distr in districts:
            return True, districts
    return False, None

def dispCityResults(goodAddress, badAddress):
    print('\nTotal: {}'.format(goodAddress + badAddress))
    print('Good:  {}'.format(goodAddress))
    print('Bad:   {}'.format(badAddress))
    print('Ratio: {}\n\n'.format(goodAddress / (goodAddress + badAddress)))
    print('All cities identified have been written to results.txt')
    print('All invalid addresses have a blank line instead')

def incrGoodAddress():
    global goodAddress
    goodAddress = goodAddress + 1

def incrBadAddress():
    global badAddress
    badAddress = badAddress + 1

def debugPrint(key, addrElements, addressCount):
    if not debug:
        return
    print(addressCount, key + '\t: ', " ".join(addrElements))
    if key == 'noValidCity':
        print(addressCount, 'noValidCity\t: ', " ".join(addrElements))


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

def cityStringParse(results, addrElements):
    matches = []
    followingWord = ''
    wordCount = len(addrElements)
    for elementIndex, origWord in enumerate(addrElements):
        if elementIndex < wordCount and elementIndex > 0:
            # Adjust for capitalization
            word = origWord.upper()[0] + origWord.lower()[1:]
            if elementIndex < wordCount - 1:
                followingWord = addrElements[elementIndex + 1].upper()[0] + addrElements[elementIndex + 1].lower()[1:]
            word = checkAbbr(word)

            if elementIndex == len(addrElements) - 1 and len(word) > 2 and word in cityList:
                matches.append(word)
            elif len(word) > 2 and followingWord not in suffixes and word in cityList:
                matches.append(word)

    # No City found, write whitespace
    if len(matches) == 0:
        debugPrint('noValidCity', addrElements, addressCount)
        writeNoCity(results)
        return

    # Remove Duplicates and write city
    matches = removeDup(matches)
    writeCity(results, matches[-1])


# ----------------------------------------------------
# Address Soruce, PostCode Map, City List and City Results
addresses = [remCommaPeriods(s.rstrip()) for s in open('dependencies/raw_addresses.txt', 'r')]
postCodeDistrictMap = {}
for postcode in [pc.rstrip().split('\t') for pc in open('dependencies/PostCodeMap.txt', 'r')]:
    postCodeDistrictMap[postcode[1]] = postcode[2]
cityList = [c.rstrip() for c in open('dependencies/'+cityListTextFile, 'r')]
results = open('results.txt', 'w')
suffixes = [s.rstrip() for s in open('dependencies/suffixes.txt', 'r')]

# START ITERATING =======================================
for addr in addresses:
    addressCount = addressCount + 1
    matchFound = False
    addrElements = addr.split()
    distr = 'NO_DISTRICT'

    # Address too short
    if len(addrElements) < 3:
        writeNoCity(results)
        if debug:
            debugPrint('tooShort', addrElements, addressCount)
        continue
    # last element length of four
    distr = addrElements[-1][0:4]  # changed
    matchFound, districts = districtFound(distr)
    if matchFound:
        if debug:
            debugPrint('last4', addrElements, addressCount)
        writeCityFromDistricts(results, districts)
        continue
    # Then try length of three
    distr = addrElements[-1][0:3]  # changed
    matchFound, districts = districtFound(distr)
    if matchFound:
        if debug:
            debugPrint('last3', addrElements, addressCount)
        writeCityFromDistricts(results, districts)
        continue
    # second to last element
    if len(addrElements) > 1:
        # second to last element length four
        distr = addrElements[-2][0:4]  # changed
        matchFound, districts = districtFound(distr)
        if matchFound:
            if debug:
                debugPrint('2tolast4', addrElements, addressCount)
            writeCityFromDistricts(results, districts)
            continue
        # Try length of three
        distr = addrElements[-2][0:3]  # changed
        matchFound, districts = districtFound(distr)
        if matchFound:
            if debug:
                debugPrint('2tolast3', addrElements, addressCount)
            writeCityFromDistricts(results, districts)
            continue
    # if all else fails (use old method)
    cityStringParse(results, addrElements)
    '''
    if debug:
        debugPrint('F',addressCount,goodAddress,badAddress,distr,addrElements)
    writeNoCity(results)
    '''

# Display at end
dispCityResults(goodAddress, badAddress)
