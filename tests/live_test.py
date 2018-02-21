# coding=utf-8
import unittest

from pynYNAB.ClientFactory import clientfromkwargs, BudgetClient
from pynYNAB.schema import DictDiffer
from pynYNAB.schema.Entity import fromapi_conversion_functions_table
from pynYNAB.schema.types import AmountType
from pynYNAB.scripts.helpers import merge_config

test_budget_name = 'Test Budget - Dont Remove'


class LiveTests2(unittest.TestCase):
    def test_roundtrip(self):
        # 1. gets sync data from server
        # 2. tests that to_api(from_api(data)) is the same thing
        kwargs = merge_config({'budget_name': test_budget_name})
        client = clientfromkwargs(sync=False, **kwargs)
        sync_data = client.catalogClient.get_sync_data_obj()
        budget_version_id = next(d['id'] for d in sync_data['changed_entities']['ce_budget_versions'] if
                                 d['version_name'] == test_budget_name)
        client.budget_version_id = budget_version_id

        for objclient in (client.budgetClient, client.catalogClient):
            sync_data = objclient.get_sync_data_obj()
            server_changed_entities = sync_data['changed_entities']

            for key in server_changed_entities:
                if key in objclient.obj.listfields:
                    if len(server_changed_entities[key]) == 0:
                        continue
                    obj_dict = server_changed_entities[key][0]
                    typ = objclient.obj.listfields[key]
                    obj_dict2 = typ.from_apidict(obj_dict).get_apidict()

                    diff = DictDiffer(obj_dict2, obj_dict)
                    for k in diff.changed():
                        AssertionError('changed {}: {}->{}'.format(k, obj_dict[k], obj_dict2[k]))
                    for k in diff.removed():
                        AssertionError('removed {}: {}'.format(k, obj_dict[k]))
                    for k in diff.added():
                        AssertionError('added {}: {}'.format(k, obj_dict2[k]))
                elif key in objclient.obj.scalarfields:
                    obj_dict2 = objclient.obj.from_apidict(server_changed_entities).get_apidict()
                    if server_changed_entities[key] != obj_dict2[key]:
                        AssertionError('changed {}: {}->{}'.format(key, server_changed_entities[key], obj_dict2[key]))


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
        kwargs = merge_config({'budget_name': test_budget_name})
        self.client = clientfromkwargs(sync=False, **kwargs)
        self.client.catalogClient.sync()
        self.client.select_budget(test_budget_name)

    def test_api_scaling_is_ok(self):
        sync_data = self.client.budgetClient.get_sync_data_obj()
        server_entities = sync_data['changed_entities']
        transactions = server_entities[BudgetClient.prefix + 'transactions']
        amount = None
        for transaction in transactions:
            if transaction['memo'] == 'TEST TRANSACTION':
                amount = fromapi_conversion_functions_table[AmountType](AmountType, transaction['amount'])
                break
        self.assertEqual(12.34, amount)
