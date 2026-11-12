"""
Author: Timothy Kornish
CreatedDate: November - 11 - 2025
Description: log into a Salesforce source org.
             query quote_line records with all fields.
             log into MSSQL staging database and
             insert records into quote_lines staging table
"""

import numpy as np
import pandas as pd
import os
from custom_db_utilities import MSSQL_Utilities, Salesforce_Utilities, Custom_Utilities
from credentials import Credentials

# create and instance of the custom salesforce utilities class used to interact with Salesforce
MSSQL_Utils = MSSQL_Utilities()
# create and instance of the custom salesforce utilities class used to interact with Salesforce
SF_Utils = Salesforce_Utilities()
# create and instance of the custom  utilities class
Utils = Custom_Utilities()
# create instance of credentials class where creds are stored to load into the script
Cred = Credentials()

# set environment to get credentials for salesforce login
sf_environment = 'Dev'
# set database to Salesforce
sf_database = "Salesforce"

# set mssql server to insert staging tables into
mssql_environment = "localhost"
# set mssql dbms parameter
mssql_dbms = "MSSQL"

# get username from credentials
sf_username = Cred.get_username(sf_database, sf_environment)
# get consumer_key from credentials
sf_consumer_key = Cred.get_consumer_key(sf_database, sf_environment)
# get privatekey_file from credentials
sf_privatekey_file = Cred.get_privatekey_file(sf_database, sf_environment)

# create a instance of simple_salesforce to query and perform operations against salesforce with
sf = SF_Utils.login_to_salesForce(username = sf_username, consumer_key = sf_consumer_key, privatekey_file = sf_privatekey_file)

# query existing quote_lines from salesforce
# query string to select records from salesforce
quote_line_query = """SELECT
	Id,
	Name,
	CreatedById,
	CreatedDate,
	IsDeleted,
	LastModifiedById,
	LastModifiedDate,
	Migrated_Record__c,
	QuoteLine_External_ID__c,
	SBQQ__AdditionalDiscount__c,
	SBQQ__AdditionalDiscountAmount__c,
	SBQQ__AdditionalQuantity__c,
	SBQQ__AllowAssetRefund__c,
	SBQQ__BatchQuantity__c,
	SBQQ__BillingFrequency__c,
	SBQQ__BillingType__c,
	SBQQ__BlockPrice__c,
	SBQQ__Bundle__c,
	SBQQ__Bundled__c,
	SBQQ__BundledQuantity__c,
	SBQQ__CarryoverLine__c,
	SBQQ__ChargeType__c,
	SBQQ__ComponentCost__c,
	SBQQ__ComponentDiscountedByPackage__c,
	SBQQ__ComponentListTotal__c,
	SBQQ__ComponentSubscriptionScope__c,
	SBQQ__ComponentTotal__c,
	SBQQ__ComponentUpliftedByPackage__c,
	SBQQ__ComponentVisibility__c,
	SBQQ__CompoundDiscountRate__c,
	SBQQ__ConfigurationRequired__c,
	SBQQ__ContractedPrice__c,
	SBQQ__Cost__c,
	SBQQ__CostEditable__c,
	SBQQ__CustomerPrice__c,
	SBQQ__CustomerTotal__c,
	SBQQ__DefaultSubscriptionTerm__c,
	SBQQ__Description__c,
	SBQQ__Dimension__c,
	SBQQ__Discount__c,
	SBQQ__DiscountSchedule__c,
	SBQQ__DiscountScheduleType__c,
	SBQQ__DiscountTier__c,
	SBQQ__DistributorDiscount__c,
	SBQQ__DynamicOptionId__c,
	SBQQ__EarliestValidAmendmentStartDate__c,
	SBQQ__EffectiveEndDate__c,
	SBQQ__EffectiveQuantity__c,
	SBQQ__EffectiveStartDate__c,
	SBQQ__EffectiveSubscriptionTerm__c,
	SBQQ__EndDate__c,
	SBQQ__Existing__c,
	SBQQ__Favorite__c,
	SBQQ__GenerateContractedPrice__c,
	SBQQ__GrossProfit__c,
	SBQQ__Group__c,
	SBQQ__Guidance__c,
	SBQQ__HasConsumptionSchedule__c,
	SBQQ__Hidden__c,
	SBQQ__Incomplete__c,
	SBQQ__ListPrice__c,
	SBQQ__ListTotal__c,
	SBQQ__Markup__c,
	SBQQ__MarkupAmount__c,
	SBQQ__MarkupRate__c,
	SBQQ__MaximumPrice__c,
	SBQQ__MinimumPrice__c,
	SBQQ__NetPrice__c,
	SBQQ__NetTotal__c,
	SBQQ__NonDiscountable__c,
	SBQQ__NonPartnerDiscountable__c,
	SBQQ__Number__c,
	SBQQ__Optional__c,
	SBQQ__OptionDiscount__c,
	SBQQ__OptionDiscountAmount__c,
	SBQQ__OptionLevel__c,
	SBQQ__OptionType__c,
	SBQQ__OriginalPrice__c,
	SBQQ__OriginalQuoteLineId__c,
	SBQQ__OriginalUnitCost__c,
	SBQQ__PackageCost__c,
	SBQQ__PackageListTotal__c,
	SBQQ__PackageProductCode__c,
	SBQQ__PackageProductDescription__c,
	SBQQ__PackageTotal__c,
	SBQQ__PartnerDiscount__c,
	SBQQ__PartnerPrice__c,
	SBQQ__PartnerTotal__c,
	SBQQ__PreviousSegmentPrice__c,
	SBQQ__PreviousSegmentUplift__c,
	SBQQ__PricebookEntryId__c,
	SBQQ__PriceEditable__c,
	SBQQ__PricingMethod__c,
	SBQQ__PricingMethodEditable__c,
	SBQQ__PriorQuantity__c,
	SBQQ__Product__c,
	SBQQ__ProductCode__c,
	SBQQ__ProductFamily__c,
	SBQQ__ProductName__c,
	SBQQ__ProductOption__c,
	SBQQ__ProductSubscriptionType__c,
	SBQQ__ProratedListPrice__c,
	SBQQ__ProratedPrice__c,
	SBQQ__ProrateMultiplier__c,
	SBQQ__Quantity__c,
	SBQQ__Quote__c,
	SBQQ__RegularPrice__c,
	SBQQ__RegularTotal__c,
	SBQQ__Renewal__c,
	SBQQ__RenewedAsset__c,
	SBQQ__RenewedSubscription__c,
	SBQQ__RequiredBy__c,
	SBQQ__SegmentIndex__c,
	SBQQ__SegmentKey__c,
	SBQQ__SegmentLabel__c,
	SBQQ__Source__c,
	SBQQ__SpecialPrice__c,
	SBQQ__SpecialPriceDescription__c,
	SBQQ__SpecialPriceType__c,
	SBQQ__StartDate__c,
	SBQQ__SubscribedAssetIds__c,
	SBQQ__SubscriptionBase__c,
	SBQQ__SubscriptionCategory__c,
	SBQQ__SubscriptionPercent__c,
	SBQQ__SubscriptionPricing__c,
	SBQQ__SubscriptionScope__c,
	SBQQ__SubscriptionTargetPrice__c,
	SBQQ__SubscriptionTerm__c,
	SBQQ__SubscriptionType__c,
	SBQQ__Taxable__c,
	SBQQ__TaxCode__c,
	SBQQ__TermDiscount__c,
	SBQQ__TermDiscountSchedule__c,
	SBQQ__TermDiscountTier__c,
	SBQQ__TotalDiscountAmount__c,
	SBQQ__TotalDiscountRate__c,
	SBQQ__UnitCost__c,
	SBQQ__UnproratedNetPrice__c,
	SBQQ__UpgradedAsset__c,
	SBQQ__UpgradedQuantity__c,
	SBQQ__UpgradedSubscription__c,
	SBQQ__Uplift__c,
	SBQQ__UpliftAmount__c,
	SBQQ__VolumeDiscount__c,
	SystemModstamp
FROM SBQQ__QuoteLine__c"""

# query salesforce and return the quote_lines to be deleted
quote_line_query_results = SF_Utils.query_salesforce(sf, quote_line_query)
# convert query results to a dataframe
sf_quote_lines_df = SF_Utils.load_query_with_lookups_into_dataframe(quote_line_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_quote_lines_df.columns = sf_quote_lines_df.columns.str.replace('.', '_', regex=False)


# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_SBQQ__QuoteLine__c'

# generate column types from passing dataframe
sf_quote_lines_dtypes = Utils.get_dtypes_as_list(sf_quote_lines_df)
# insert subset of the csv  from a dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_quote_lines_df, sf_quote_lines_dtypes, drop_table = True)
