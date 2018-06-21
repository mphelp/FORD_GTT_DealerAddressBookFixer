### Author: Matthew Phelps, Updated: June 19 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

from functions import *
from addressInfo import addressInfo

# Variables
badAddress = 0  # valid addresses
goodAddress = 0  # invalid addresses
addressCount = 4  # for debugging, 5 is first index of column
DEBUG = True  # examine invalid addresses
cityListTextFile = 'GTNcityList.txt'
resultsFile = 'results.txt'
hasOffset = True

# ----------------------------------------------------
# Address Soruce, PostCode Map, City List and City Results
addresses = [remComma(s.rstrip()) for s in open('dependencies/raw_addresses.txt', 'r')]
postCodeDistrictMap = {}
for postcode in [pc.rstrip().split('\t') for pc in open('dependencies/PostCodeMap.txt', 'r')]:
    postCodeDistrictMap[postcode[1]] = postcode[2]
cityList = [c.rstrip() for c in open('dependencies/'+cityListTextFile, 'r')]
cityListLower = [c.lower() for c in cityList]
suffixes = [s.rstrip() for s in open('dependencies/suffixes.txt', 'r')]


# START ITERATING =======================================
addrInfo = addressInfo(resultsFile=resultsFile,hasOffset=hasOffset)
for addr in addresses:
    addrInfo.incrCurrentIndex()
    matchFound = False
    addrElements = addr.split()
    potentialDistricts = [addrElements[-1][0:4],addrElements[-1][0:3],
                          addrElements[-2][0:4],addrElements[-2][0:3]]
    # Address too short
    if len(addrElements) < 3:
        addrInfo.writeNoCity()
        debugPrint(DEBUG, 'tooShort', addrElements, addrInfo.currentAddrIndex)
        continue
    # last element length of four distr = addrElements[-1][0:4]  # changed
    # last element length of three
    # second to last element of four
    # second to last element of three
    for distr in potentialDistricts:
        foundCityFromPostCode, city = postCodeLookup(distr, postCodeDistrictMap)
        if foundCityFromPostCode and city.lower() in cityListLower:
            debugPrint(DEBUG, distr, addrElements, addrInfo.currentAddrIndex)
            addrInfo.writeCity(city)
            break
    if not foundCityFromPostCode:
        foundCityFromAddrStr, city = cityStringParse()
        if foundCityFromAddrStr:
            debugPrint()
            addrInfo.
        # check EVERY string in cityListLower whether or not it is in addr string
        #stringMatches = cityStringParse(addrElements, addrInfo.currentAddrIndex)

# Display at end
addrInfo.dispCityResults()

'''
    matchFound, city = cityFound(distr,postCodeDistrictMap)
    if matchFound:
        debugPrint(DEBUG, 'last4', addrElements, addressCount)
        # write city
        continue
    # Then try length of three
    distr = addrElements[-1][0:3]  # changed
    matchFound, city = cityFound(distr,postCodeDistrictMap)
    if matchFound:
        debugPrint(DEBUG, 'last3', addrElements, addressCount)
        # write city
        continue
    # second to last element
    if len(addrElements) > 1:
        # second to last element length four
        distr = addrElements[-2][0:4]  # changed
        matchFound, districts = districtFound(distr,postCodeDistrictMap)
        if matchFound:
            debugPrint(DEBUG,'2tolast4', addrElements, addressCount)
            writeCityFromDistricts(results, districts)
            continue
        # Try length of three
        distr = addrElements[-2][0:3]  # changed
        matchFound, districts = districtFound(distr,postCodeDistrictMap)
        if matchFound:
            debugPrint(DEBUG,'2tolast3', addrElements, addressCount)
            writeCityFromDistricts(results, districts)
            continue
    # if all else fails (use old method)
    cityStringParse(results, addrElements)
    '''
