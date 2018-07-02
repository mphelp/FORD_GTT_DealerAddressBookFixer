### Author: Matthew Phelps, Updated: June 25 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

######### NOTES:
# Poland is an acceptable city.
# Need a list of exceptions.

from myUtil import AddrStats, parse, Timer
from myUtil import GTNAddressLookup, IncompleteGlobalDealerAddresses, CompleteGlobalDealerAddresses
import pandas as pd
import numpy as np
import xlrd
import time
import openpyxl

# Vars

incompleteAddrExcel = 'dependencies/20180620 GTT Dealers with Incomplete address.xlsx'
incompleteSheetName = 'Address Data city is inappropri'
approvedGTNAddrExcel = 'dependencies/GTNexus_CityList_20180208.xlsx'
completeAddrExcel = 'CorrectedGlobalGTTDealerAddresses.xlsx'

# Instantiate Incomplete/Complete

incomplete = IncompleteGlobalDealerAddresses.IncompleteGlobalDealerAddresses(incompleteAddrExcel=incompleteAddrExcel,
                                                                             incompleteSheetName=incompleteSheetName)
incomplete.loadIncompleteAddrFields()
complete = CompleteGlobalDealerAddresses.CompleteGlobalDealerAddresses(completeAddrExcel=completeAddrExcel)
complete.copyIncompleteAddrDFasTemplate(incomplete.incompleteAddrDF)
complete.addPostChangeDescriptorColumns()
values = pd.Series([i for i in range(1582)])
print([i for i in complete.completeAddrDF])

print(f'New City Column: {complete.CityNewIndex}')

# Instantiate Approved


# Begin iteration
'''
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
'''
##### TO DO
'''
Classes:
FinalAddrExcel - write all columns (new and old) to excel file
                - auto fill excel file
GTNAddressLookup - load and store all accepted address details
                  - lookup function to see if city/country is in dataframe
IncompleteGTTAddr - load and store all incomplete GTT address details
                   - store a log of successes/failures
                   - record current position of parsing

'''