import pandas as pd
from pathlib import Path
import win32com.client as win32

class FormattedExcelWriter:

    def __init__(self):
        pass
    def writeDFToExcelAndFormatProperly(self, dataframe, config):
        # Write to excel
        dataframe.to_excel(config.completeAddrExcel)
        # Autofill excel
        completedAddrExcelFULLPATH = Path(config.completeAddrExcel).absolute()
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(completedAddrExcelFULLPATH)
        ws = wb.Worksheets("Sheet1")
        ws.Columns.AutoFit()
        wb.Save()
        excel.Application.Quit()



