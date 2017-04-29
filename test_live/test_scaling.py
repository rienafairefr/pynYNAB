# -*- coding: utf-8 -*-
import unittest
from pynYNAB.ClientFactory import clientfromargs
from pynYNAB.__main__ import parser
from pynYNAB.schema.Entity import toapi_conversion_functions_table, fromapi_conversion_functions_table
from pynYNAB.schema.types import AmountType

test_budget_name = 'Test Budget - Dont Remove'


# this test cases expect that
# a budget named "Test Budget" exists
# in it, there is an account named "Account"
# in it there is a transaction date 27/01/2017 that has inflow == 12.34 € with a memo "TEST TRANSACTION"
# We check the API dict we fetch when syncing budget
class LiveTestBudget(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(LiveTestBudget, self).__init__(*args, **kwargs)
        self.transaction = None
        self.client = None

    def setUp(self):
        args = parser.parse_known_args()[0]
        args.budgetname = test_budget_name
        self.client = clientfromargs(args, sync=False)
        self.client.catalogClient.sync()
        self.client.select_budget(test_budget_name)

    def test_api_scaling_is_ok(self):
        sync_data = self.client.budgetClient.get_sync_data_obj()
        server_entities = sync_data['changed_entities']
        transactions = server_entities['be_transactions']
        amount = None
        for transaction in transactions:
            if transaction['memo'] == 'TEST TRANSACTION':
                amount = fromapi_conversion_functions_table[AmountType](transaction['amount'])
        self.assertEqual(12.34,amount)
