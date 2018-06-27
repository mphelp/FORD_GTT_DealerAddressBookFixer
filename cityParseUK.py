### Author: Matthew Phelps, Updated: June 25 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

import Lib.parse as parse
import Lib.addrStats as addrStats

# Variables
badAddress = 0  # valid addresses
goodAddress = 0  # invalid addresses
debug = True  # examine invalid addresses
debugAll = False  # print all written lines
cityListTextFile = 'dependencies/GTNcityList.txt'
resultsFile = 'results.txt'  # where cities are written to
hasOffset = False  # excel row offset

# ----------------------------------------------------
# Address Source, PostCode Map, City List and City Results
addresses = [parse.remPunctuation(s.rstrip()) for s in open('dependencies/raw_addresses.txt', 'r')]
postCodeDistrictMap = {}
for postcode in [pc.rstrip().split('\t') for pc in open('dependencies/PostCodeMap.txt', 'r')]:
    postCodeDistrictMap[postcode[1]] = postcode[2]
cityList = [c.rstrip() for c in open(cityListTextFile, 'r')]
cityListSimplified = [parse.remPunctuation(c.lower()) for c in cityList]
suffixes = [s.rstrip() for s in open('dependencies/suffixes.txt', 'r')]

# START ITERATING =======================================

# Address Info object
addrInfoUK = addrStats.addrStats(resultsFile=resultsFile, hasOffset=hasOffset, debug=debug, debugAll=debugAll)
for addr in addresses:
    # Setup
    addrInfoUK.incrCurrentIndex()
    addrElements = addr.split()
    foundCityFromAddrStr, foundCityFromPostCode = False, False

    # Address too short
    if len(addrElements) <= 3:
        addrInfoUK.debugPrint(addrElements, distr='  ', key='tooShort')
        addrInfoUK.writeNoCity()
        continue
    potentialDistricts = [addrElements[-1][0:4], addrElements[-1][0:3],
                          addrElements[-2][0:4], addrElements[-2][0:3]]

    # Method 1: Iterate through post code districts in address
    for distr in potentialDistricts:
        foundCityFromPostCode, cityFromPC = parse.postCodeLookup(distr, postCodeDistrictMap,
                                                                 cityList, cityListSimplified)
        if foundCityFromPostCode:
            addrInfoUK.debugPrint(addrElements, distr=distr, key=cityFromPC)
            addrInfoUK.writeCity(cityFromPC)
            break
    # Method 2: Iterate through the address string for city
    if not foundCityFromPostCode:
        foundCityFromAddrStr, cityFromStr = parse.cityStringParse(addr, cityList,
                                                                  cityListSimplified)
        if foundCityFromAddrStr:
            addrInfoUK.debugPrint(addrElements, distr='  ', key=cityFromStr)
            addrInfoUK.writeCity(cityFromStr)
        else:
            # No city found with either method
            addrInfoUK.debugPrint(addrElements, distr='  ', key='noValidCity')
            addrInfoUK.writeNoCity()

# Display at end
addrInfoUK.dispCityResults()
