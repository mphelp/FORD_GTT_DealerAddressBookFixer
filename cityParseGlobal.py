### Author: Matthew Phelps, Updated: July 2 2018
###         IT Application Development Intern
###         iTek Center, Red Wolves skill team
###         Ford Motor Company

from myUtil.AddressImporter import AddressImporter
from myUtil.Configuration import Configuration
from myUtil.Address import Address
from myUtil import Timer
from myUtil.FormattedExcelWriter import FormattedExcelWriter
from myUtil.GTNAddressLookup import GTNAddressLookup
from myUtil.IncompleteGlobalDealerAddresses import IncompleteGlobalDealerAddresses
from myUtil.CompleteGlobalDealerAddresses import CompleteGlobalDealerAddresses
import pandas as pd
from myUtil import parse
import numpy as np

## File configuration (edit the class to change file locations, names, or excel sheets)
config = Configuration()


## Create Virtual GTN Address Book
myTimer = Timer.Timer()
myTimer.start('Create Virtual GTN Address Book')
approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(config.approvedGTNAddrExcel), config.approvedGTNSheetName)
ai = AddressImporter()
addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(approvedAddressesDataFrame)
myTimer.end()

# (In)complete address lists setup
myTimer.start('Load incomplete addresses from ' + config.incompleteAddrExcel)
incomplete = IncompleteGlobalDealerAddresses(config)
complete = CompleteGlobalDealerAddresses(config)
complete.copyIncompleteAddrDFasTemplateAndAddColumns(incomplete.incompleteAddrDF)
myTimer.end()

## Begin iteration over address list
myTimer.start('Iteration and lookup')
for index, addressData in complete.completeAddrDF.iterrows():
    lookup = GTNAddressLookup()

    thisAddr = Address(city=addressData.loc['City'],
                               countryName=addressData.loc['Country Name'],
                               add1=addressData.loc['Address 1'],
                               add2=addressData.loc['Address 2'],
                               postalCode=addressData.loc['Postal Code'],
                               locationName=addressData.loc['Location Name'])

    # City
    cities = []
    for addressElement in [thisAddr.city, thisAddr.locationName, thisAddr.add1, thisAddr.add2]:
        cityFoundFromLookup = lookup.lookupCity(addressElement,addressBook)
        cities.append(cityFoundFromLookup)
    existingEntry = False
    for word in cities:
        if word:
            existingEntry = True
    realCities = [parse.convertToStr(c) for c in cities]
    if existingEntry:
        complete.completeAddrDF.loc[index][[config.citySuggestionColumnTitle]] = ', '.join(realCities)
        complete.completeAddrDF.loc[index][[config.cityIdentifiedColumnTitle]] = 'Yes'
myTimer.end()

## Write to excel
myTimer.start('Write to new excel file ' + config.completeAddrExcel)
ew = FormattedExcelWriter()
ew.writeDFToExcelAndFormatProperly(complete.completeAddrDF, config)
myTimer.end()
