### Author: Matthew Phelps, Updated: July 2 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

######### NOTES:
# Poland is an acceptable city.
# Need a list of exceptions.
from myUtil.AddressImporter import AddressImporter
from myUtil.Configuration import Configuration
from myUtil import Timer, Address
from myUtil import GTNAddressLookup, IncompleteGlobalDealerAddresses, CompleteGlobalDealerAddresses
import pandas as pd

config = Configuration()

## Instantiate Incomplete/Complete
approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(config.approvedGTNAddrExcel),
                                                   config.approvedGTNSheetName)

ai = AddressImporter(config.approvedGTNAddrExcel, config.approvedGTNSheetName)
addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(approvedAddressesDataFrame)

myTimer = Timer.Timer()
myTimer.start('Instantiate Incomplete/Complete and load, copy, and add new columns')
incomplete = IncompleteGlobalDealerAddresses.IncompleteGlobalDealerAddresses(incompleteAddrExcel=config.incompleteAddrExcel,
                                                                             incompleteSheetName=config.incompleteSheetName)
incomplete.loadIncompleteAddrFields()
complete = CompleteGlobalDealerAddresses.CompleteGlobalDealerAddresses(completeAddrExcel=completeAddrExcel)
complete.copyIncompleteAddrDFasTemplate(incomplete.incompleteAddrDF)
complete.addPostChangeDescriptorColumns()
myTimer.end()

## Instantiate Approved

myTimer.start('Instantiate Approved and load')

config = Configuration()
approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(config.approvedAddressesFile),
                                                   config.approvedSheetName)
approved = GTNAddressLookup.GTNAddressLookup(approvedAddressesFile=approvedGTNAddrExcel,
                                             approvedSheetName=approvedGTNSheetName)

myTimer.end()

# Begin iteration

myTimer.start('Iteration')
for index, addressData in complete.completeAddrDF.iterrows():

    thisAddr = Address.Address(city=addressData.loc['City'],
                               countryName=addressData.loc['Country Name'],
                               add1=addressData.loc['Address 1'],
                               add2=addressData.loc['Address 2'],
                               postalCode=addressData.loc['Postal Code'])

    thisAddr.__repr__()
    print(approved.lookupCity(thisAddr.city))
myTimer.end()



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