Feature: Fix all the Addresses
  Scenario: Basic validation
    Given An Approved Address List
     When we process a list of Addresses
     Then we should get a list of good Addresses