### Author: Matthew Phelps, Updated: June 22 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

from postCodeUtil import *
from addrStrUtil import *
from addressInfo import addressInfo

# Variables
badAddress = 0      # valid addresses
goodAddress = 0     # invalid addresses
debug = True        # examine invalid addresses
debugAll = False    # print all written lines
cityListTextFile = 'dependencies/GTNcityList.txt'
resultsFile = 'results.txt' # where cities are written to
hasOffset = False   # excel row offset

# ----------------------------------------------------
# Address Soruce, PostCode Map, City List and City Results
addresses = [remPunctuation(s.rstrip()) for s in open('dependencies/raw_addresses.txt', 'r')]
postCodeDistrictMap = {}
for postcode in [pc.rstrip().split('\t') for pc in open('dependencies/PostCodeMap.txt', 'r')]:
    postCodeDistrictMap[postcode[1]] = postcode[2]
cityList = [c.rstrip() for c in open(cityListTextFile, 'r')]
cityListSimplified = [remPunctuation(c.lower()) for c in cityList]
suffixes = [s.rstrip() for s in open('dependencies/suffixes.txt', 'r')]


# START ITERATING =======================================

# Address Info object
addrInfo = addressInfo(resultsFile=resultsFile, hasOffset=hasOffset, debug=debug, debugAll=debugAll)
for addr in addresses:
    # Setup
    addrInfo.incrCurrentIndex()
    addrElements = addr.split()
    foundCityFromAddrStr, foundCityFromPostCode = False, False

    # Address too short
    if len(addrElements) <= 3:
        addrInfo.debugPrint(addrElements, distr='  ', key='tooShort')
        addrInfo.writeNoCity()
        continue
    potentialDistricts = [addrElements[-1][0:4],addrElements[-1][0:3],
                          addrElements[-2][0:4],addrElements[-2][0:3]]

    # Method 1: Iterate through post code districts in address
    for distr in potentialDistricts:
        foundCityFromPostCode, cityFromPC = postCodeLookup(distr, postCodeDistrictMap,
                                                           cityList, cityListSimplified)
        if foundCityFromPostCode:
            addrInfo.debugPrint(addrElements, distr=distr, key=cityFromPC)
            addrInfo.writeCity(cityFromPC)
            break
    # Method 2: Iterate through the address string for city
    if not foundCityFromPostCode:
        foundCityFromAddrStr, cityFromStr = cityStringParse(addr, cityList,
                                                            cityListSimplified)
        if foundCityFromAddrStr:
            addrInfo.debugPrint(addrElements, distr='  ', key=cityFromStr)
            addrInfo.writeCity(cityFromStr)
        else:
            # No city found with either method
            addrInfo.debugPrint(addrElements, distr='  ', key='noValidCity')
            addrInfo.writeNoCity()

# Display at end
addrInfo.dispCityResults()
