"""
Author: Timothy Kornish
CreatedDate: November - 11 - 2025
Description: log into a Salesforce source org.
             query quote records with all fields.
             log into MSSQL staging database and
             insert records into quotes staging table
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

# query existing quotes from salesforce
# query string to select records from salesforce
quote_query = """SELECT
	Id,
	Name,
	CreatedById,
	CreatedDate,
	IsDeleted,
	LastActivityDate,
	LastModifiedById,
	LastModifiedDate,
	LastReferencedDate,
	LastViewedDate,
	Migrated_Record__c,
	OwnerId,
	Quote_External_ID__c,
	SBQQ__Account__c,
	SBQQ__AdditionalDiscountAmount__c,
	SBQQ__AverageCustomerDiscount__c,
	SBQQ__AveragePartnerDiscount__c,
	SBQQ__BillingCity__c,
	SBQQ__BillingCountry__c,
	SBQQ__BillingFrequency__c,
	SBQQ__BillingName__c,
	SBQQ__BillingPostalCode__c,
	SBQQ__BillingState__c,
	SBQQ__BillingStreet__c,
	SBQQ__ConsumptionRateOverride__c,
	SBQQ__ContractingMethod__c,
	SBQQ__CustomerAmount__c,
	SBQQ__CustomerDiscount__c,
	SBQQ__DaysQuoteOpen__c,
	SBQQ__DefaultTemplate__c,
	SBQQ__DeliveryMethod__c,
	SBQQ__Distributor__c,
	SBQQ__DistributorDiscount__c,
	SBQQ__DocumentStatus__c,
	SBQQ__EmailTemplateId__c,
	SBQQ__EndDate__c,
	SBQQ__ExpirationDate__c,
	SBQQ__FirstSegmentTermEndDate__c,
	SBQQ__GenerateContractedPrice__c,
	SBQQ__Introduction__c,
	SBQQ__Key__c,
	SBQQ__LastCalculatedOn__c,
	SBQQ__LastSavedOn__c,
	SBQQ__LineItemCount__c,
	SBQQ__LineItemsGrouped__c,
	SBQQ__LineItemsPrinted__c,
	SBQQ__ListAmount__c,
	SBQQ__MarkupRate__c,
	SBQQ__MasterContract__c,
	SBQQ__MasterEvergreenContract__c,
	SBQQ__NetAmount__c,
	SBQQ__Notes__c,
	SBQQ__Opportunity2__c,
	SBQQ__OrderBy__c,
	SBQQ__OrderByQuoteLineGroup__c,
	SBQQ__Ordered__c,
	SBQQ__OrderGroupID__c,
	SBQQ__OriginalQuote__c,
	SBQQ__PaperSize__c,
	SBQQ__Partner__c,
	SBQQ__PartnerDiscount__c,
	SBQQ__PaymentTerms__c,
	SBQQ__PriceBook__c,
	SBQQ__PricebookId__c,
	SBQQ__Primary__c,
	SBQQ__PrimaryContact__c,
	SBQQ__ProrationDayOfMonth__c,
	SBQQ__QuoteLanguage__c,
	SBQQ__QuoteProcessId__c,
	SBQQ__QuoteTemplateId__c,
	SBQQ__RegularAmount__c,
	SBQQ__RenewalTerm__c,
	SBQQ__RenewalUpliftRate__c,
	SBQQ__SalesRep__c,
	SBQQ__ShippingCity__c,
	SBQQ__ShippingCountry__c,
	SBQQ__ShippingName__c,
	SBQQ__ShippingPostalCode__c,
	SBQQ__ShippingState__c,
	SBQQ__ShippingStreet__c,
	SBQQ__Source__c,
	SBQQ__StartDate__c,
	SBQQ__Status__c,
	SBQQ__SubscriptionTerm__c,
	SBQQ__TargetCustomerAmount__c,
	SBQQ__TotalCustomerDiscountAmount__c,
	SBQQ__Type__c,
	SBQQ__Uncalculated__c,
	SBQQ__Unopened__c,
	SBQQ__WatermarkShown__c,
	SystemModstamp
FROM SBQQ__Quote__c
WHERE Migrated_Record__c = true"""

# query salesforce and return the quotes to be deleted
quote_query_results = SF_Utils.query_salesforce(sf, quote_query)
# convert query results to a dataframe
sf_quotes_df = SF_Utils.load_query_with_lookups_into_dataframe(quote_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_quotes_df.columns = sf_quotes_df.columns.str.replace('.', '_', regex=False)

# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_SBQQ__Quote__c'

# drop table if already exists;
drop_table_sql =  f"""USE [{mssql_environment}] SET ANSI_NULLS ON SET QUOTED_IDENTIFIER ON;
                    DROP TABLE IF EXISTS {table_name}; """

# execute sql
MSSQL_Utils.execute_sql(mssql_connection, mssql_cursor, drop_table_sql)

# generate column types from passing dataframe
sf_quotes_dtypes = Utils.get_dtypes_as_list(sf_quotes_df)
# insert sf records dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_quotes_df, sf_quotes_dtypes, drop_table = True, db_name = mssql_environment)
