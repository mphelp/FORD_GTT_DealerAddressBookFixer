### Author: Matthew Phelps, Updated: June 25 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

######### NOTES:
# Poland is an acceptable city.
# Need a list of exceptions.

from lib import parse, AddrStats, Timer
import pandas as pd
import numpy as np
import xlrd
import time

# Vars
globalResultsFile = 'resultsGlobal.txt'
incompleteAddrExcel = 'dependencies/20180620 GTT Dealers with Incomplete address.xlsx'
incompleteSheetName = 'Address Data city is inappropri'
approvedGTNAddrExcel = 'dependencies/GTNexus_CityList_20180208.xlsx'
debugAll = False
hasOffSet = False

# Source, I/O Read Write
myTimer = Timer.Timer()
myTimer.start('Excel Loading')
incompleteAddrTable = pd.read_excel(pd.ExcelFile(incompleteAddrExcel), incompleteSheetName)
approvedGTNAddrTable = pd.read_excel(approvedGTNAddrExcel)
AddrInfoGlobal = AddrStats.AddrStats(resultsFile=globalResultsFile,debugAll=debugAll,hasOffset=hasOffSet)
myTimer.end()

# List Setup
myTimer.start('List Setup')
incompleteAddrCityList = [parse.convertToStr(getattr(addr, 'City'))
                          for addr in incompleteAddrTable[['City']].itertuples()]
approvedGTNAddrCityList = [parse.convertToStr(getattr(addr, 'City'))
                           for addr in approvedGTNAddrTable[['City']].itertuples()]
approvedGTNAddrCityListSimplified = [parse.remPunctuation(c.lower()) for c in approvedGTNAddrCityList]
myTimer.end()

# Begin iteration
myTimer.start('Iteration')
for possibleCity in incompleteAddrCityList:
    matchFound, correctCity = parse.cityStringParse(possibleCity, approvedGTNAddrCityList,
                                                    approvedGTNAddrCityListSimplified)
    if matchFound:
        AddrInfoGlobal.writeCity(correctCity)
        AddrInfoGlobal.debugPrint(possibleCity)
    else:
        AddrInfoGlobal.writeNoCity()
        AddrInfoGlobal.debugPrint(possibleCity)
myTimer.end()

# Display results
AddrInfoGlobal.dispCityResults()