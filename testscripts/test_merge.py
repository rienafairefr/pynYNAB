import unittest

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema import BudgetVersion
from pynYNAB.schema import Transaction


class DummyConnection(object):
    id = '12345'

    def __init__(self):
        self.transactions = []

    def dorequest(self, request_data, opname):
        d = dict(server_knowledge_of_device=0, current_server_knowledge=42)
        if opname == 'syncBudgetData':
            changed = dict(transactions=[tr.get_apidict() for tr in self.transactions],
                                                master_categories=[],
                                                settings=[],
                                                monthly_budget_calculations=[],
                                                account_mappings=[],
                                                subtransactions=[],
                                                scheduled_subtransactions=[],
                                                monthly_budgets=[],
                                                subcategories=[],
                                                payee_locations=[],
                                                account_calculations=[],
                                                monthly_account_calculations=[],
                                                monthly_subcategory_budget_calculations=[],
                                                scheduled_transactions=[],
                                                payees=[],
                                                monthly_subcategory_budgets=[],
                                                payee_rename_conditions=[],
                                                accounts=[])


            d.update(dict(changed_entities=dict(last_month='',
                                                first_month='')))
        elif opname == 'syncCatalogData':
            d.update(dict(changed_entities=dict(ce_user_budgets=[],
                                                ce_user_settings=[],
                                                ce_budget_versions=[BudgetVersion(version_name='Test').get_apidict()],
                                                ce_users=[],
                                                ce_budgets=[])))

        return d

import time
elapsed = []
for size in [10, 20, 40, 70, 100, 200, 400, 700,1000, 2000, 4000]:
    connection = DummyConnection()
    connection.transactions=[Transaction(memo=str(i)) for i in range(size)]
    client = nYnabClientFactory().create_client(connection=connection, budget_name='Test', sync=False)

    t = time.time()
    # do stuff
    client.sync()
    time_elapsed = time.time() - t
    elapsed.append(round(time_elapsed, 1))
    assert (set(client.budget.transactions) == set(connection.transactions))
    print('%i,%f' % (size, time_elapsed))
print(','.join(str(i) for i in elapsed))

