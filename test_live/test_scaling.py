# -*- coding: utf-8 -*-
import unittest
from pynYNAB.Client import clientfromargs
from pynYNAB.scripts.config import parser

test_budget_name = 'Test Budget'


# this test cases expect that
# a budget named "Test Budget" exists
# in it, there is an account named "Account"
# in it there is a transaction date 27/01/2017 that has inflow == 10 € with a memo "TEST TRANSACTION"
# We check the API dict we fetch when syncing budget
class LiveTestBudget(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(LiveTestBudget, self).__init__(*args, **kwargs)
        self.transaction = None
        self.client = None

    def setUp(self):
        args = parser.parse_known_args()[0]
        self.client = clientfromargs(args, sync=False)
        self.client.sync_catalog()
        self.client.select_budget(test_budget_name)

    def api_scaling_is_1000(self):
        sync_data = self.client.budgetClient.get_sync_data_obj(extra=dict(
                          calculated_entities_included=False,
                          budget_version_id=self.client.budget_version_id))
        server_entities = sync_data['changed_entities']
        transactions = server_entities['be_transactions']
        scaling = None
        for transaction in transactions:
            if transaction['memo'] == 'TEST TRANSACTION':
                scaling = int(transaction['amount']/10)
        self.assertEqual(1000,scaling)
