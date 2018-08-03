import pandas as pd
import numpy as np
import xlrd
import openpyxl

# Vars
globalResultsFile = 'resultsGlobal.txt'
incompleteAddrExcel = '../dependencies/20180620 GTT Dealers with Incomplete address.xlsx'
incompleteSheetName = 'Address Data city is inappropri'
approvedGTNAddrExcel = '../dependencies/GTNexus_CityList_20180208.xlsx'
completedAddrExcel = 'CompleteAddresses.xlsx'

# Read in excel
incompleteAddrDF = pd.read_excel(pd.ExcelFile(incompleteAddrExcel), incompleteSheetName)
# Write to excel
incompleteAddrDF.to_excel(completedAddrExcel)

# Autofill excel
from pathlib import Path
import win32com.client as win32
completedAddrExcelFULLPATH = Path(completedAddrExcel).absolute()
excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(completedAddrExcelFULLPATH)
ws = wb.Worksheets("Sheet1")
ws.Columns.AutoFit()
wb.Save()
excel.Application.Quit()



