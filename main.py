# coding=utf-8
import configparser
import sys
from budget import Transaction
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
    transaction=Transaction()
    transaction.accepted=True
    transaction.amount=666
    transaction.cleared='Cleared'
    transaction.credit_amount=666
    transaction.entities_account_id=nYNABobject.budgets[0].be_accounts[0].id
    transaction.entities_payee_id=nYNABobject.budgets[0].be_payees[0].id
    transaction.entities_subcategory_id=nYNABobject.budgets[0].be_subcategories[0].id
    transaction.is_tombstone=False

    nYNABobject.budgets[0].be_transactions.append(transaction)
    nYNABobject.budgets[0].current_knowledge += 1

    nYNABobject.sync()


if __name__ == "__main__":
    if 'test' in sys.argv:
        import doctest
        doctest.testmod()
    addtransaction()

