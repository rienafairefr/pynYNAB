=====
Usage
=====

Canonical client creation
-------------------------

A way to create a client and fetch data::

    from pynYNAB.Client import nYnabClient

    client = nYnabClient(email="############", password="######", budgetname='TestBudget')
    client.sync()

You can also decouple the connection and session management from the client object::

    connection = nYnabConnection(email, password)
    connection.init_session()
    client = nYnabClient(nynabconnection=connection, budgetname='TestBudget')
    client.sync()


Local database
--------------

Once data is downloaded from the servers, it is stored in a local database, accessed through sqlAlchemy.
All the relations between objects are in here through appropriate One-to-Many or Many-to-One relations, etc.


Client factory
--------------

A YNAB client (of type nYnabClient\_) is just another object that can be persisted in the database.
The nYnabClient( [...] ) --without the \_-- constructor is just a wrapper around calling
nYnabClientFactory().create_client( [...] )

The ClientFactory initializes the database, just pass it an engine URL, like::

    from pynYNAB.ClientFactory import ClientFactory
    factory = ClientFactoy('sqlite:////tmp/persist.db')
    client1 = factory.create_client(email=***,password=***,budget_name=***)
    [ do something with data in client1 ]
    client2 = factory.create_client(email=***,password=***,budget_name=***)

These two clients will be strictly identical, referring to the same client in the database, so client2
will contain the modifications done in client1

Pushing entities
----------------

In order to sync data to the YNAB servers, we need to know how much data we want to push.
We don't need to construct the array of data to push, this is all done transparently
for you in the background through sqlAlchemy modification hooks.

Here we add two transactions and one payee, then push them::

    client.sync()
    client.budget.be_transactions.append(transaction1)
    client.budget.be_transactions.append(transaction2)
    client.budget.be_payees.append(payee)
    client.budget.push(3)

With the first sync, the amount of currently modified data is reset to 0, and the additions of data are tracked

Previously, you could accidentally push a modification that erased all your YNAB data. Now the `push` method stops you
from doing that, by limiting the modifications to at most 1 entity if no paramaters are passed.


Database query
--------------

We can use the sqlAlchemy backend in order to get interesting views to the data::

    from sqlalchemy.sql import func
    from datetime import datetime
    session = client.session

    # sum of the amounts for all transactions younger than 10 weeks
    session.query(func.sum(Transaction.amount)).filter(Transaction.date > datetime.datetime.now() - datetime.timedelta(weeks=10)).scalar()

    # sum of the amounts for each month
    session.query(func.strftime('%Y-%m',Transaction.date),func.sum(Transaction.amount)).group_by(extract('month',Transaction.date)).all()

    # same for positive amounts only
    session.query(func.strftime('%Y-%m',Transaction.date),func.sum(Transaction.amount)).filter(Transaction.amount>0).group_by(extract('month',Transaction.date)).all()

    # see the total of the transactions, grouping per-payee
    session.query(func.sum(Transaction.amount),Transaction.amount).group_by(Transaction.entities_payee).join(Payee).all()

Everything is possible, see sqlAlchemy docs :-)


