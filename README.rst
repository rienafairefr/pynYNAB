.. image:: https://secure.travis-ci.org/rienafairefr/nYNABapi.png
    :target: http://travis-ci.org/rienafairefr/nYNABapi

.. image:: https://coveralls.io/repos/github/rienafairefr/nYNABapi/badge.svg?branch=master
   :target: https://coveralls.io/github/rienafairefr/nYNABapi?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target:  https://pypi.python.org/pypi/pynYNAB


========
nYNABapi
========

a python client for the new YNAB API

Installation
------------

download the source, then call `python setup.py install`

Usage
-----

Either code your own script that uses the pynYNAB api, or use the provided scripts, ofximport, YNAB4 migrate, csvimport

Scripts Documentation
---------------------

see appropriate `README`_

API Documentation
-----------------

nYNAB is organised around a root object, here it is a nYnabClient object. It is created by giving it a connection object,
which handles the requests to the server (app.youneedabudget.com and its api endpoint /api/v1/catalog),
using the same commands that the Javascript app at app.youneedabudget.com uses internally.

The connection object needs email and password for the nYNAB account

Once you have created your nYnabClient object, all data should have already been synced up with YNAB's servers. If you
need the updated data from the server, call sync on the nYnabClient.

All the entity handling is done through the Budget and Catalog objects, they contain collections such
as be_accounts, be_transactions, ce_user_settings, etc. Look into the budget/catalog for the schema.

In order to write some data to YNAB servers for your budget, you just need to modify those Budget/Catalog
objects then call nYnabobject.push . all the subcollections like ce_budget_transactions support append, remove, etc,
like normal lists.

push takes an expected_delta argument, this is to safeguard modifying too much of your data on the server by error.
Examples:
* if you add two matched transactions to be_transactions, then the expected delta is 2
* If you add a single payee, then the expected delta is 1


I've provided some tested methods e.g. add_account, add_transaction, in the nYnabClient class to
add/delete accounts and transactions as examples. Some actions are not always simple (e.g., to add an account, 
you need to add a transfer payee, a starting balance transaction, otherwise the server refuses the request). You're welcome 
to contribute new actions e.g. by catching the requests done in the UI with Fiddler to see what's done.

Caution with add_transaction, it works even for large amount of transactions (tested up to 3000), but please 
don't stress test the YNAB servers with it...

Approach of preventing Harm  
---------------------------

I've taken all precautionary steps so that this python Client can't affect YNAB even if used too widely. 
* It honors requests by the server to throttle its requests  >  Same mechanisme that the JS app uses
* It self-limits the requests to 5 request per second 
* It clearly identifies itself by User-Agent > Easy to lock it out if it causes trouble



.. _README: https://github.com/rienafairefr/nYNABapi/blob/master/scripts/README.rst
