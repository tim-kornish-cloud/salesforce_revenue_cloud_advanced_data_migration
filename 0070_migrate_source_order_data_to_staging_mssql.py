"""
Author: Timothy Kornish
CreatedDate: November - 11 - 2025
Description: log into a Salesforce source org.
             query order records with all fields.
             log into MSSQL staging database and
             insert records into orders staging table
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

# query existing orders from salesforce
# query string to select records from salesforce
order_query = """SELECT
	Id,
	Name,
	AccountId,
	ActivatedById,
	ActivatedDate,
	BillingAddress,
	BillingCity,
	BillingCountry,
	BillingGeocodeAccuracy,
	BillingLatitude,
	BillingLongitude,
	BillingPostalCode,
	BillingState,
	BillingStreet,
	BillToContactId,
	CompanyAuthorizedById,
	CompanyAuthorizedDate,
	ContractId,
	CreatedById,
	CreatedDate,
	CustomerAuthorizedById,
	CustomerAuthorizedDate,
	Description,
	EffectiveDate,
	EndDate,
	IsDeleted,
	IsReductionOrder,
	LastModifiedById,
	LastModifiedDate,
	LastReferencedDate,
	LastViewedDate,
	OpportunityId,
	OrderNumber,
	OrderReferenceNumber,
	OriginalOrderId,
	OwnerId,
	PoDate,
	PoNumber,
	Pricebook2Id,
	SBQQ__Contracted__c,
	SBQQ__ContractingMethod__c,
	SBQQ__OrderBookings__c,
	SBQQ__PaymentTerm__c,
	SBQQ__PriceCalcStatus__c,
	SBQQ__PriceCalcStatusMessage__c,
	SBQQ__Quote__c,
	SBQQ__RenewalTerm__c,
	SBQQ__RenewalUpliftRate__c,
	SBQQ__TaxAmount__c,
	ShippingAddress,
	ShippingCity,
	ShippingCountry,
	ShippingGeocodeAccuracy,
	ShippingLatitude,
	ShippingLongitude,
	ShippingPostalCode,
	ShippingState,
	ShippingStreet,
	ShipToContactId,
	Status,
	StatusCode,
	SystemModstamp,
	TotalAmount,
	Type
FROM Order"""

# query salesforce and return the orders to be deleted
order_query_results = SF_Utils.query_salesforce(sf, order_query)
# convert query results to a dataframe
sf_orders_df = SF_Utils.load_query_with_lookups_into_dataframe(order_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_orders_df.columns = sf_orders_df.columns.str.replace('.', '_', regex=False)


# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_Order'

# generate column types from passing dataframe
sf_orders_dtypes = Utils.get_dtypes_as_list(sf_orders_df)
# insert subset of the csv  from a dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_orders_df, sf_orders_dtypes, drop_table = True)
