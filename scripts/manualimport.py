import argparse

import re
from ofxtools import OFXTree

from pynYNAB.connection import nYnabConnection
from pynYNAB.budget import Transaction, Payee
from pynYNAB.config import email, password
from pynYNAB.Client import nYnabClient, BudgetNotFound

parser = argparse.ArgumentParser(description='Manually import an OFX into a nYNAB budget')
parser.add_argument('ofxfile', metavar='OFXPath', type=str,
                    help='The OFX file to import')
parser.add_argument('budgetname', metavar='BudgetName', type=str,
                    help='The budget to create')


args=parser.parse_args()

connection = nYnabConnection(email, password, reload=True)

tree=OFXTree()
tree.parse(args.ofxfile)
response = tree.convert()
stmts = response.statements

try:
    nYNABobject = nYnabClient(connection, budget_name=args.budgetname, reload=True)
except BudgetNotFound:
    print('No budget by this name found in nYNAB')
    exit(-1)

accounts=nYNABobject.budget.be_accounts
reKey=re.compile('.*key\[(?P<key>.*)\]key')
keystoaccounts={reKey.match(account.note).group('key'):account for account in accounts if account.note!=None}


for stmt in stmts:
    key=stmt.account.bankid + ' ' + stmt.account.branchid + ' ' + stmt.account.bankid
    if key not in keystoaccounts:
        # ask user input for which bank this is, then save it into the account note in nYNAB
        for iaccount,account in enumerate(accounts):
            print('#%d %s'%(iaccount,account.account_name))
        while True:
            accountnumber=input('Which account is this OFX for? ')
            try:
                accountnumber=int(accountnumber)
                if accountnumber >= 0 and accountnumber <= len(accounts)-1:
                    break
            except ValueError:
                pass
            print('Please enter a number between %d and %d'%(0,len(accounts)-1))
        account=accounts[accountnumber]

        # Save the selection in the nYNAB account note
        addon='key[' + key +']key'
        if account.note is not None:
            account.note += addon
        else:
            account.note = addon
        nYNABobject.budget.be_accounts.modify(account)
        nYNABobject.sync()

    account=keystoaccounts[key]

    for ofx_transaction in stmt.transactions:
        payee_name = ofx_transaction.name if ofx_transaction.payee is None else ofx_transaction.payee

        # use ftid so we don't import duplicates
        if not any(ofx_transaction.fitid in transaction.memo for transaction in nYNABobject.budget.be_transactions if transaction.memo is not None):
            transaction=Transaction(
                date=ofx_transaction.dtposted,
                memo=ofx_transaction.memo + ofx_transaction.fitid,
                imported_payee=payee_name,
                amount=float(ofx_transaction.trnamt),
                entities_account_id=account.id
            )
            nYNABobject.add_transaction(transaction)


