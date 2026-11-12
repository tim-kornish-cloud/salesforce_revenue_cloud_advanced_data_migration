"""
Author: Timothy Kornish
CreatedDate: November - 11 - 2025
Description: log into a Salesforce source org.
             query contract records with all fields.
             log into MSSQL staging database and
             insert records into contracts staging table
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

# query existing contracts from salesforce
# query string to select records from salesforce
contract_query = """SELECT
	Id,
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
	CompanySignedDate,
	CompanySignedId,
	ContractNumber,
	ContractTerm,
	CreatedById,
	CreatedDate,
	CustomerSignedDate,
	CustomerSignedId,
	CustomerSignedTitle,
	Description,
	EndDate,
	IsDeleted,
	LastActivityDate,
	LastApprovedDate,
	LastModifiedById,
	LastModifiedDate,
	LastReferencedDate,
	LastViewedDate,
	OwnerExpirationNotice,
	OwnerId,
	Pricebook2Id,
	SBQQ__ActiveContract__c,
	SBQQ__AmendmentOpportunityRecordTypeId__c,
	SBQQ__AmendmentOpportunityStage__c,
	SBQQ__AmendmentOwner__c,
	SBQQ__AmendmentPricebookId__c,
	SBQQ__AmendmentRenewalBehavior__c,
	SBQQ__AmendmentStartDate__c,
	SBQQ__DefaultRenewalContactRoles__c,
	SBQQ__DefaultRenewalPartners__c,
	SBQQ__DisableAmendmentCoTerm__c,
	SBQQ__Evergreen__c,
	SBQQ__ExpirationDate__c,
	SBQQ__MasterContract__c,
	SBQQ__MDQRenewalBehavior__c,
	SBQQ__Opportunity__c,
	SBQQ__OpportunityPricebookId__c,
	SBQQ__Order__c,
	SBQQ__PreserveBundleStructureUponRenewals__c,
	SBQQ__Quote__c,
	SBQQ__RenewalForecast__c,
	SBQQ__RenewalOpportunity__c,
	SBQQ__RenewalOpportunityRecordTypeId__c,
	SBQQ__RenewalOpportunityStage__c,
	SBQQ__RenewalOwner__c,
	SBQQ__RenewalPricebookId__c,
	SBQQ__RenewalQuoted__c,
	SBQQ__RenewalTerm__c,
	SBQQ__RenewalUpliftRate__c,
	SBQQ__SubscriptionQuantitiesCombined__c,
	SpecialTerms,
	StartDate,
	Status,
	StatusCode,
	SystemModstamp
FROM Contract"""

# query salesforce and return the contracts to be deleted
contract_query_results = SF_Utils.query_salesforce(sf, contract_query)
# convert query results to a dataframe
sf_contracts_df = SF_Utils.load_query_with_lookups_into_dataframe(contract_query_results)

# since shipping address and billing address infor is comprised of multiple fields
# that are returned with a .
# this throws an error when inserting to mssql,
# change to underscore for continuity
sf_contracts_df.columns = sf_contracts_df.columns.str.replace('.', '_', regex=False)

# initiate an MS SQL connection and cursor to query with
mssql_connection, mssql_cursor = MSSQL_Utils.login_to_mssql(server = Cred.get_server(dbms = mssql_dbms, env = mssql_environment),
                                                            database = Cred.get_database(dbms = mssql_dbms, env = mssql_environment))

# mssql table name the dataframe is being inserted into
table_name = 'SF_CPQ_STG_Contract'

# generate column types from passing dataframe
sf_contracts_dtypes = Utils.get_dtypes_as_list(sf_contracts_df)
# insert sf records dataframe into the mssql table
MSSQL_Utils.upload_reports(mssql_connection, mssql_cursor, table_name, sf_contracts_df, sf_contracts_dtypes, drop_table = True, db_name = mssql_environment)
