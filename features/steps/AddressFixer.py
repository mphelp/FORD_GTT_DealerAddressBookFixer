from behave import *
from nose.tools import assert_equal

from myUtil.AddressImporter import AddressImporter
from myUtil.Configuration import Configuration


@given('An Approved Address List')
def step_impl(context):
    config = Configuration()
    approvedAddressesDataFrame = pd.read_excel(pd.ExcelFile(config.approvedGTNAddrExcel), config.approvedGTNSheetName)
    ai = AddressImporter()
    context.addressBook = ai.loadGTNApprovedAddressesCitiesAndCountries(approvedAddressesDataFrame)

@when('we process a list of Addresses')
def step_impl(context):
    # read the bad addressses from the given excel file
    context.results = processAddresses()

@then('we should get a list of good Addresses')
def step_impl(context):
    assert_equal(len(context.results), 3) 
    assert_equal(context.results[0].city, "London") 
    