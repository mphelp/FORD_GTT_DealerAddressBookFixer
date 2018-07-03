import pandas as pd
import numpy as np
from myUtil import parse
from myUtil.Configuration import Configuration

class CompleteGlobalDealerAddresses:
    def __init__(self, config):
        self.completeAddrExcel = config.completeAddrExcel

    def copyIncompleteAddrDFasTemplateAndAddColumns(self, incompleteDF):
        self.completeAddrDF = incompleteDF.copy(deep=True)
        self.addPostChangeDescriptorColumns()

    def addPostChangeDescriptorColumns(self):
        emptyColumn = ['' for i in range(len(self.completeAddrDF))]
        self.CityNewIndex = self.completeAddrDF.columns.get_loc('City') + 1
        self.completeAddrDF.insert(loc=self.CityNewIndex, column='New City', value=emptyColumn)
        self.CityChangedIndex = self.completeAddrDF.columns.get_loc('New City') + 1
        self.completeAddrDF.insert(loc=self.CityChangedIndex, column='City Changed?', value=emptyColumn)
        self.CountryNewIndex = self.completeAddrDF.columns.get_loc('Country Name') + 1
        self.completeAddrDF.insert(loc=self.CountryNewIndex, column='New Country', value=emptyColumn)
        self.CountryChangedIndex = self.completeAddrDF.columns.get_loc('New Country') + 1
        self.completeAddrDF.insert(loc=self.CountryChangedIndex, column='Country Changed?', value=emptyColumn)




