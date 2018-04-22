import unittest

import pytest

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
            d.update(dict(changed_entities=dict(transactions=[tr.get_apidict() for tr in self.transactions],
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
                                                accounts=[],
                                                last_month='',
                                                first_month='')))
        elif opname == 'syncCatalogData':
            d.update(dict(changed_entities=dict(user_budgets=[],
                                                user_settings=[],
                                                budget_versions=[BudgetVersion(version_name='Test').get_apidict()],
                                                users=[],
                                                budgets=[])))

        return d


@pytest.fixture
def connection():
    return DummyConnection()


def test_merge(connection):
    connection.transactions=[Transaction(memo=str(i)) for i in range(51)]
    client = nYnabClientFactory().create_client(connection=connection, budget_name='Test', sync=False)
    client.sync()
    assert set(client.budget.transactions) == set(connection.transactions)
