import pandas as pd
from myUtil import parse

class IncompleteGlobalDealerAddresses:
    def __init__(self, incompleteAddrExcel = 'Please specify file path', incompleteSheetName = 'Specify sheet name'):
        self.incompleteAddrExcel = incompleteAddrExcel
        self.incompleteSheetName = incompleteSheetName

    def loadIncompleteAddrFields(self):
        self.incompleteAddrDF = pd.read_excel(pd.ExcelFile(self.incompleteAddrExcel), self.incompleteSheetName)
