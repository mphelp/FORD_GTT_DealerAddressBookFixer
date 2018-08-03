import pandas as pd
from myUtil import parse
from myUtil.Configuration import Configuration

class IncompleteGlobalDealerAddresses:
    def __init__(self, config):
        self.incompleteAddrExcel = config.incompleteAddrExcel
        self.incompleteSheetName = config.incompleteSheetName
        self.loadIncompleteAddrFields()

    def loadIncompleteAddrFields(self):
        self.incompleteAddrDF = pd.read_excel(pd.ExcelFile(self.incompleteAddrExcel), self.incompleteSheetName)
