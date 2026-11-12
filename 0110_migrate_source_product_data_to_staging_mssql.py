"""
Author: Timothy Kornish
CreatedDate: November - 11 - 2025
Description: log into a Salesforce source org.
             query product records with all fields.
             log into MSSQL staging database and
             insert records into products staging table
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
mssql_environment = "RCA_Migration"
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

# query existing products from salesforce
# query string to select records from salesforce
product_query = """SELECT
	Id,
	Name,
	CreatedById,
	CreatedDate,
	Description,
	DisplayUrl,
	ExternalDataSourceId,
	ExternalId,
	Family,
	IsActive,
	IsArchived,
	IsDeleted,
	LastModifiedById,
	LastModifiedDate,
	LastReferencedDate,
	LastViewedDate,
	ProductCode,
	QuantityUnitOfMeasure,
	SBQQ__AssetAmendmentBehavior__c,
	SBQQ__AssetConversion__c,
	SBQQ__BatchQuantity__c,
	SBQQ__BillingFrequency__c,
	SBQQ__BillingType__c,
	SBQQ__BlockPricingField__c,
	SBQQ__ChargeType__c,
	SBQQ__Component__c,
	SBQQ__CompoundDiscountRate__c,
	SBQQ__ConfigurationEvent__c,
	SBQQ__ConfigurationFields__c,
	SBQQ__ConfigurationFieldSet__c,
	SBQQ__ConfigurationFormTitle__c,
	SBQQ__ConfigurationType__c,
	SBQQ__ConfigurationValidator__c,
	SBQQ__ConfiguredCodePattern__c,
	SBQQ__ConfiguredDescriptionPattern__c,
	SBQQ__CostEditable__c,
	SBQQ__CostSchedule__c,
	SBQQ__CustomConfigurationPage__c,
	SBQQ__CustomConfigurationRequired__c,
	SBQQ__CustomerCommunityAvailability__c,
	SBQQ__DefaultPricingTable__c,
	SBQQ__DefaultQuantity__c,
	SBQQ__DescriptionLocked__c,
	SBQQ__DiscountCategory__c,
	SBQQ__DiscountSchedule__c,
	SBQQ__DynamicPricingConstraint__c,
	SBQQ__EnableLargeConfiguration__c,
	SBQQ__ExcludeFromMaintenance__c,
	SBQQ__ExcludeFromOpportunity__c,
	SBQQ__ExternallyConfigurable__c,
	SBQQ__GenerateContractedPrice__c,
	SBQQ__HasConfigurationAttributes__c,
	SBQQ__HasConsumptionSchedule__c,
	SBQQ__Hidden__c,
	SBQQ__HidePriceInSearchResults__c,
	SBQQ__IncludeInMaintenance__c,
	SBQQ__NewQuoteGroup__c,
	SBQQ__NonDiscountable__c,
	SBQQ__NonPartnerDiscountable__c,
	SBQQ__Optional__c,
	SBQQ__OptionLayout__c,
	SBQQ__OptionSelectionMethod__c,
	SBQQ__PriceEditable__c,
	SBQQ__PricingGuidance__c,
	SBQQ__PricingMethod__c,
	SBQQ__PricingMethodEditable__c,
	SBQQ__ProductPictureID__c,
	SBQQ__QuantityEditable__c,
	SBQQ__QuantityScale__c,
	SBQQ__ReconfigurationDisabled__c,
	SBQQ__RenewalProduct__c,
	SBQQ__SortOrder__c,
	SBQQ__Specifications__c,
	SBQQ__SubscriptionBase__c,
	SBQQ__SubscriptionCategory__c,
	SBQQ__SubscriptionPercent__c,
	SBQQ__SubscriptionPricing__c,
	SBQQ__SubscriptionTarget__c,
	SBQQ__SubscriptionTerm__c,
	SBQQ__SubscriptionType__c,
	SBQQ__Taxable__c,
	SBQQ__TaxCode__c,
	SBQQ__TermDiscountLevel__c,
	SBQQ__TermDiscountSchedule__c,
	SBQQ__UpgradeCredit__c,
	SBQQ__UpgradeRatio__c,
	SBQQ__UpgradeSource__c,
	SBQQ__UpgradeTarget__c,
	StockKeepingUnit,
	SystemModstamp
FROM Product2"""

# query salesforce and return the products to be deleted
product_query_results = SF_Utils.query_salesforce(sf, product_query)
# convert query results to a dataframe
sf_products_df = SF_Utils.load_query_with_lookups_into_dataframe(product_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_products_df.columns = sf_products_df.columns.str.replace('.', '_', regex=False)

# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_Product2'

# generate column types from passing dataframe
sf_products_dtypes = Utils.get_dtypes_as_list(sf_products_df)
# insert sf records dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_products_df, sf_products_dtypes, drop_table = True, db_name = mssql_environment)
