import unittest

import yaml

from pynYNAB.ClientFactory import clientfromkwargs
from pynYNAB.schema import DictDiffer
from pynYNAB.schema.budget import Transaction
from pynYNAB.scripts.helpers import get_config_from_env, merge_config
from .common import CommonLive
from .common import needs_account


# noinspection PyArgumentList
class LiveTests(CommonLive):
    @needs_account()
    def test_add_deletetransaction(self):
        from datetime import datetime
        transaction = Transaction(
            amount=1,
            cleared='Uncleared',
            date=datetime.now(),
            entities_account_id=self.account.id,
        )
        self.client.add_transaction(transaction)
        self.reload()
        self.assertIn(transaction, self.client.budget.transactions)
        self.client.delete_transaction(transaction)
        self.reload()
        self.assertNotIn(transaction, self.client.budget.transactions)


test_budget_name = 'Test Budget - Dont Remove'


class LiveTests2(unittest.TestCase):
    def test_roundtrip(self):
        config = merge_config()
        client = clientfromkwargs(sync=False, **config)

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


if __name__ == "__main__":
    unittest.main()
