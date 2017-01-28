import random
from datetime import datetime, timedelta

from pynYNAB import KeyGenerator
from pynYNAB.schema.Entity import AccountTypes
from pynYNAB.schema.budget import Transaction, Account, Subtransaction, Payee
from test_live.common import CommonLive
from test_live.common import needs_account


# noinspection PyArgumentList
class LiveTests(CommonLive):
    def test_roundtrip(self):
        # 1. syncs data from server
        # 2. gets the pushed changed_entities that would be pushed as if all entities were modified
        # 3 the pushed changed_entities should be strictly identical to the changed_entities that was received

        def get_changed_entities_current(obj):
            current_map = obj.getmaps()
            return {k: list(v.values()) if isinstance(v,dict) else v  for k,v in current_map.items()}

        def clean_id_tombstoned(ce):
            returnvalue = {}
            for k, value in ce.items():
                if k == 'is_tombstone' or k == 'id':
                    continue

                if isinstance(value,list):
                    returnvalue[k] = list(set(v for v in value if not v.is_tombstone))
            return returnvalue

        server_catalog_changed_entities = clean_id_tombstoned(self.client.server_entities['syncCatalogData'])
        server_budget_changed_entities = clean_id_tombstoned(self.client.server_entities['syncBudgetData'])

        pushed_catalog_changed_entities = clean_id_tombstoned(get_changed_entities_current(self.client.catalog))
        pushed_budget_changed_entities = clean_id_tombstoned(get_changed_entities_current(self.client.budget))

        self.checkEqual(pushed_catalog_changed_entities.keys(), server_catalog_changed_entities.keys(),
                        'catalog changed entities roundtrip keys %s and %s not equal')
        self.checkEqual(pushed_budget_changed_entities.keys(), server_budget_changed_entities.keys(),
                        'budget changed entities roundtrip keys not equal')

        for key in server_catalog_changed_entities:
            self.checkEqual(pushed_catalog_changed_entities[key], server_catalog_changed_entities[key],
                            'catalog changed entities roundtrip value for key %s not equal' % key)
        for key in server_budget_changed_entities:
            self.checkEqual(pushed_budget_changed_entities[key], server_budget_changed_entities[key],
                            'budget changed entities roundtrip value for key %s not equal' % key)

    @staticmethod
    def checkEqual(l1, l2, msg):
        ll1 = list(l1)
        ll2 = list(l2)
        try:
            if len(ll1) == len(ll2) and len(set(ll1) - set(ll2)) == 0:
                return True
        except TypeError as e:
            pass
        raise AssertionError(msg)