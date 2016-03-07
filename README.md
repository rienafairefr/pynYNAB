# nYNABapi

a python client for the new YNAB API

# Installation

download the source, then call `python setup.py install`

# Usage

Either code your own script that uses the pynYNAB api, or use the provided scripts, ofximport and YNAB4 migrate

# Scripts Documentation

After install, you should be able to call ofximport and nmigrate scripts, you either pass the email/password
 as command line arguments or modify the ynab.conf file (Which should be created in some place dependent on your OS if 
 the script can't find it).

# API Documentation

nYNAB is organised around a root object, here it is a nYnabClient object. It is created by giving it a connection object,
which handles the requests to the server (app.youneedabudget.com and its api endpoint /api/v1/catalog),
using the same commands that the Javascript app app.youneedabudget.com uses internally.

The connection object needs email and password for the nYNAB account

Once you have created your nYnabClient object, all data should have already been synced up with YNAB's servers

All the entity handling is done through the Budget and Catalog objects, which contain collections such
as be_accounts, be_transactions, ce_user_settings, etc.

In order to write some data to YNAB servers for your budget, you just need to modify a collection in those Budget/Catalog
 objects then call nYnabobject.sync . To append a new entity, delete or modify an existing one, call the appropriate 
  methods on a collection inside the budget or catalog objects.
    
 I've provided some tested methods e.g. add_account, add_transaction, in the nYnabClient class to
add/delete accounts and transactions as examples.

Caution with add_transaction, it works even for large amount of transactions (tested up to 3000), but please don't stress test
the YNAB servers with it... Recently (I think), YNAB implemented throttling on their API, and pynYNAB honors it, by 
catching request_throttled errors and waiting the time specified in the  Retry-After header
