# nYNABapi

a python client for the new YNAB API

The nYNAB API is organised around a root object, here it is the nYnab object. It is created by giving it an nYnabconnection,
which handles the requests to the server (app.youneedabudget.com and its api endpoint /api/v1/catalog),
using the same commands that the Javascript app uses.

Once you have created your nYNAB object, all data should have already been synced up.

Here all the knowledge/entity hanlding is done through the Budget and Catalog objects, which contain collections such
as be_accounts, be_transactions, ce_user_settings, etc.

In order to write some data to YNAB servers for your budget, you just need to modify a collection in those Budget/Catalog
 objects then call nYnabobject.sync . I've provided some tested methods e.g. add_account, add_transaction, in the nYnab object to
add/delete accounts and transactions as examples.

Caution with add_transaction, it works even for large amount of transactions (tested up to 3000), but please don't stress test
the YNAB servers with it...
