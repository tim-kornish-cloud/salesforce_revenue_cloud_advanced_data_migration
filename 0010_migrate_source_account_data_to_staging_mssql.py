"""
Author: Timothy Kornish
CreatedDate: November - 10 - 2025
Description: log into a Salesforce source org.
             query account records with all fields.
             log into MSSQL staging database and
             insert records into accounts staging table
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

# query existing accounts from salesforce
# query string to select records from salesforce
account_query = """SELECT
	Id,
	Name,
	Account_Number_External_ID__c,
	AccountNumber,
	AccountSource,
	Active__c,
	AnnualRevenue,
	BillingAddress,
	BillingCity,
	BillingCountry,
	BillingGeocodeAccuracy,
	BillingLatitude,
	BillingLongitude,
	BillingPostalCode,
	BillingState,
	BillingStreet,
	CleanStatus,
	CreatedById,
	CreatedDate,
	CustomerPriority__c,
	DandbCompanyId,
	Description,
	DunsNumber,
	Fax,
	Industry,
	IsDeleted,
	Jigsaw,
	JigsawCompanyId,
	LastActivityDate,
	LastModifiedById,
	LastModifiedDate,
	LastReferencedDate,
	LastViewedDate,
	MasterRecordId,
	Migrated_Record__c,
	NaicsCode,
	NaicsDesc,
	NumberOfEmployees,
	NumberofLocations__c,
	OwnerId,
	Ownership,
	ParentId,
	Phone,
	PhotoUrl,
	Rating,
	SBQQ__AssetQuantitiesCombined__c,
	SBQQ__ContractCoTermination__c,
	SBQQ__CoTermedContractsCombined__c,
	SBQQ__CoTerminationEvent__c,
	SBQQ__DefaultOpportunity__c,
	SBQQ__IgnoreParentContractedPrices__c,
	SBQQ__PreserveBundle__c,
	SBQQ__PriceHoldEnd__c,
	SBQQ__RenewalModel__c,
	SBQQ__RenewalPricingMethod__c,
	SBQQ__TaxExempt__c,
	ShippingAddress,
	ShippingCity,
	ShippingCountry,
	ShippingGeocodeAccuracy,
	ShippingLatitude,
	ShippingLongitude,
	ShippingPostalCode,
	ShippingState,
	ShippingStreet,
	Sic,
	SicDesc,
	Site,
	SLA__c,
	SLAExpirationDate__c,
	SLASerialNumber__c,
	SystemModstamp,
	TickerSymbol,
	Tradestyle,
	Type,
	UpsellOpportunity__c,
	Website,
	YearStarted
FROM Account"""

# query salesforce and return the accounts to be deleted
account_query_results = SF_Utils.query_salesforce(sf, account_query)
# convert query results to a dataframe
sf_accounts_df = SF_Utils.load_query_with_lookups_into_dataframe(account_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_accounts_df.columns = sf_accounts_df.columns.str.replace('.', '_', regex=False)

# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_Accounts'

# generate column types from passing dataframe
sf_accounts_dtypes = Utils.get_dtypes_as_list(sf_accounts_df)
# insert sf records dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_accounts_df, sf_accounts_dtypes, drop_table = True, db_name = mssql_environment)
