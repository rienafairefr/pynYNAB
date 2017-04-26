from memory_profiler import memory_usage, profile
from sqlalchemy import create_engine

from pynYNAB.Client import clientfromargs
from pynYNAB.schema.budget import Transaction


class Args(object):
    email='email'
    password='password'
    nynabconnection=None
    budgetname='test budget'

client = clientfromargs(Args(),sync=False)
#client.session.bind.echo = True

@profile
def func():
    print('test_sync')
    for i in range(0,5000):
        client.budget.be_transactions.append(Transaction())
    client.session.commit()
    client.budget.clear_changed_entities()
    print('Entities in the client: %i'%(sum([len(getattr(client.budget, f)) for f in client.budget.listfields]) +
          sum([len(getattr(client.catalog, f)) for f in client.catalog.listfields])))
    pass

if __name__ == '__main__':
    func()




