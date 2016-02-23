# coding=utf-8
import configparser
import sys
from budget import Transaction, Account, Payee
from nYNAB import nYNAB
from nYNABConnection import nYNABConnection

cp = configparser.ConfigParser()
cp.read("ynab.conf")
email = cp.get('AUTHENTICATION', 'email')
password = cp.get('AUTHENTICATION', 'password')

connection = nYNABConnection(email, password, reload=True)
nYNABobject = nYNAB(connection, reload=True)

# the catalog is where non budget specific things are stored, like users, settings, budget names
# budgets is a list of the budgets, each one contains transactions, etc

#test succesive syncs
def successivesyncs():
    """
     >>> successivesyncs()
     0
     0
     0
    """
    print(nYNABobject.catalog.knowledge)
    nYNABobject.sync()
    print(nYNABobject.catalog.knowledge)
    nYNABobject.sync()
    print(nYNABobject.catalog.knowledge)

# if we want to modify an entity and send its modification to the server and to have it accepted:

def addtransaction():
    from datetime import datetime
    k0=nYNABobject.budgets.keys()[0]

    transaction=Transaction.create(
        accepted=True,
        amount=666,
        cash_amount=0,
        cleared='Uncleared',
        date=datetime.now().strftime('%Y-%m-%d'),
        credit_amount=0,
        entities_account_id=nYNABobject.budgets[k0].be_accounts[0].id,
        entities_payee_id=None,
        entities_subcategory_id=None,
        is_tombstone=False
    )
    nYNABobject.budgets[k0].be_transactions.append(transaction)
    nYNABobject.budgets[k0].current_knowledge += 1

    nYNABobject.sync()

def addaccount():
    k0=nYNABobject.budgets.keys()[0]
    budget=nYNABobject.budgets[k0]

    sortable_index=max([account.sortable_index for account in budget.be_accounts])
    account=Account.create(
        account_type="Checking",
        account_name="Checking",
        on_budget=True,
        hidden=False,
        is_tombstone=False,
        sortable_index=sortable_index,
        direct_connect_enabled=False
    )

    payee=Payee.create(
        entities_account_id=account.id,
        enabled=True,
        is_tombstone=False,
        auto_fill_subcategory_enabled=True,
        auto_fill_memo_enabled=False,
        auto_fill_amount_enabled=False,
        rename_on_import_enabled=False,
        name="Transfer : %s" % account.account_name
    )
    immediateincomeid=None
    for sub in budget.be_subcategories:
        if sub.internal_name=='Category/__ImmediateIncome__':
            immediateincomeid=sub.id


    from datetime import datetime
    transaction=Transaction.create(
        accepted=True,
        amount=0,
        entities_subcategory_id=immediateincomeid,
        cash_amount=0,
        cleared='Cleared',
        date=datetime.now().strftime('%Y-%m-%d'),
        entities_account_id=account.id,
        credit_amount=0
    )

    startingBalanceid=None
    for p in nYNABobject.budgets[k0].be_payees:
        if p.internal_name=='StartingBalancePayee':
            startingBalanceid=p.id

    transaction.entities_account_id=account.id
    transaction.entities_payee_id=startingBalanceid
    transaction.entities_subcategory_id=None
    transaction.is_tombstone=False


    nYNABobject.budgets[k0].be_accounts.append(account)
    nYNABobject.budgets[k0].be_payees.append(payee)
    nYNABobject.budgets[k0].be_transactions.append(transaction)
    nYNABobject.budgets[k0].current_knowledge += 3


    nYNABobject.sync()


if __name__ == "__main__":
    if 'test' in sys.argv:
        import doctest
        doctest.testmod()
    addaccount()

