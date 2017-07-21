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
            d.update(dict(changed_entities=dict(be_transactions=[tr.get_apidict() for tr in self.transactions],
                                                be_master_categories=[],
                                                be_settings=[],
                                                be_monthly_budget_calculations=[],
                                                be_account_mappings=[],
                                                be_subtransactions=[],
                                                be_scheduled_subtransactions=[],
                                                be_monthly_budgets=[],
                                                be_subcategories=[],
                                                be_payee_locations=[],
                                                be_account_calculations=[],
                                                be_monthly_account_calculations=[],
                                                be_monthly_subcategory_budget_calculations=[],
                                                be_scheduled_transactions=[],
                                                be_payees=[],
                                                be_monthly_subcategory_budgets=[],
                                                be_payee_rename_conditions=[],
                                                be_accounts=[],
                                                last_month='',
                                                first_month='')))
        elif opname == 'syncCatalogData':
            d.update(dict(changed_entities=dict(ce_user_budgets=[],
                                                ce_user_settings=[],
                                                ce_budget_versions=[BudgetVersion(version_name='Test').get_apidict()],
                                                ce_users=[],
                                                ce_budgets=[])))

        return d


class TestMerge(unittest.TestCase):
    def test_merge(self):
        connection = DummyConnection()
        connection.transactions=[Transaction(memo=str(i)) for i in range(51)]
        client = nYnabClientFactory().create_client(connection=connection, budget_name='Test', sync=False)
        client.sync()
        self.assertEqual(set(client.budget.be_transactions),set(connection.transactions))
