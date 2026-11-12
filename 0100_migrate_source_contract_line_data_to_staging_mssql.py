"""
Author: Timothy Kornish
CreatedDate: November - 11 - 2025
Description: log into a Salesforce source org.
             query subscription records with all fields.
             log into MSSQL staging database and
             insert records into subscriptions staging table
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

# query existing subscriptions from salesforce
# query string to select records from salesforce
subscription_query = """SELECT
	Id,
	Name,
	CreatedById,
	CreatedDate,
	IsDeleted,
	LastModifiedById,
	LastModifiedDate,
	OwnerId,
	SBQQ__Account__c,
	SBQQ__AdditionalDiscountAmount__c,
	SBQQ__BillingFrequency__c,
	SBQQ__BillingType__c,
	SBQQ__Bundle__c,
	SBQQ__Bundled__c,
	SBQQ__BundledQuantity__c,
	SBQQ__ChargeType__c,
	SBQQ__ComponentDiscountedByPackage__c,
	SBQQ__ComponentSubscriptionScope__c,
	SBQQ__Contract__c,
	SBQQ__ContractNumber__c,
	SBQQ__CreditProductId__c,
	SBQQ__CustomerPrice__c,
	SBQQ__Dimension__c,
	SBQQ__DimensionType__c,
	SBQQ__Discount__c,
	SBQQ__DiscountSchedule__c,
	SBQQ__DiscountScheduleType__c,
	SBQQ__DistributorDiscount__c,
	SBQQ__DynamicOptionId__c,
	SBQQ__EndDate__c,
	SBQQ__HasConsumptionSchedule__c,
	SBQQ__ListPrice__c,
	SBQQ__MarkupAmount__c,
	SBQQ__MarkupRate__c,
	SBQQ__NetPrice__c,
	SBQQ__Number__c,
	SBQQ__OptionDiscount__c,
	SBQQ__OptionDiscountAmount__c,
	SBQQ__OptionLevel__c,
	SBQQ__OptionType__c,
	SBQQ__OrderProduct__c,
	SBQQ__OriginalQuoteLine__c,
	SBQQ__OriginalUnitCost__c,
	SBQQ__PackageProductCode__c,
	SBQQ__PackageProductDescription__c,
	SBQQ__PartnerDiscount__c,
	SBQQ__PricingMethod__c,
	SBQQ__Product__c,
	SBQQ__ProductId__c,
	SBQQ__ProductName__c,
	SBQQ__ProductOption__c,
	SBQQ__ProductSubscriptionType__c,
	SBQQ__ProrateMultiplier__c,
	SBQQ__Quantity__c,
	SBQQ__QuoteLine__c,
	SBQQ__RegularPrice__c,
	SBQQ__RenewalPrice__c,
	SBQQ__RenewalProductId__c,
	SBQQ__RenewalProductOptionId__c,
	SBQQ__RenewalProductOptionProductId__c,
	SBQQ__RenewalProductOptionSubscriptionPricing__c,
	SBQQ__RenewalQuantity__c,
	SBQQ__RenewalUpliftRate__c,
	SBQQ__RenewedDate__c,
	SBQQ__RequiredById__c,
	SBQQ__RequiredByProduct__c,
	SBQQ__RevisedSubscription__c,
	SBQQ__RootId__c,
	SBQQ__SegmentEndDate__c,
	SBQQ__SegmentIndex__c,
	SBQQ__SegmentKey__c,
	SBQQ__SegmentLabel__c,
	SBQQ__SegmentQuantity__c,
	SBQQ__SegmentStartDate__c,
	SBQQ__SegmentUplift__c,
	SBQQ__SegmentUpliftAmount__c,
	SBQQ__SpecialPrice__c,
	SBQQ__StartDate__c,
	SBQQ__SubscriptionEndDate__c,
	SBQQ__SubscriptionPricing__c,
	SBQQ__SubscriptionStartDate__c,
	SBQQ__SubscriptionType__c,
	SBQQ__TermDiscountSchedule__c,
	SBQQ__TerminatedDate__c,
	SBQQ__UnitCost__c,
	SystemModstamp
FROM SBQQ__Subscription__c"""

# query salesforce and return the subscriptions to be deleted
subscription_query_results = SF_Utils.query_salesforce(sf, subscription_query)
# convert query results to a dataframe
sf_subscriptions_df = SF_Utils.load_query_with_lookups_into_dataframe(subscription_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_subscriptions_df.columns = sf_subscriptions_df.columns.str.replace('.', '_', regex=False)


# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_SBQQ__Subscription__c'

# generate column types from passing dataframe
sf_subscriptions_dtypes = Utils.get_dtypes_as_list(sf_subscriptions_df)
# insert subset of the csv  from a dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_subscriptions_df, sf_subscriptions_dtypes, drop_table = True)
