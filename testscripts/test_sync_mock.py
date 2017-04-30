import json
import timeit
import unittest

from sqlalchemy import create_engine

from pynYNAB.ClientFactory import nYnabClientFactory, BudgetClient
from pynYNAB.schema import Budget, Transaction


class TestSyncMock(unittest.TestCase):
    def test_sync_mock(self):
        class MockConnection(object):
            user_id='1'

            def dorequest(self, request_data, opname):
                with open(opname+'.json','r') as f:
                    data = json.load(f)
                    return data
        engine = create_engine('sqlite://',echo=True)
        client = nYnabClientFactory(engine=engine).create_client(budgetname='Test Budget',
                                                                 connection = MockConnection(),
                                                                 sync=True)

    def test_update_obj(self):
        class MockConnection():
            user_id = '2'

        memos_index = range(150)
        memos = [str(i) for i in memos_index]

        def case1():
            data = {'be_transactions': [Transaction(memo=str(i)) for i in memos_index]}
            engine = create_engine('sqlite://', echo=True)
            client = nYnabClientFactory(engine=engine).create_client(budgetname='Test Budget',
                                                                     connection=MockConnection,
                                                                     new=True,
                                                                     sync=False)
            client.budgetClient.update_from_changed_entities(data)
            updated_memos = [tr.memo for tr in client.budget.be_transactions]
            self.assertItemsEqual(memos,updated_memos)

        def case2():
            data = {'be_transactions': [Transaction(memo=str(i)).get_dict() for i in memos_index]}
            engine = create_engine('sqlite://', echo=True)
            client = nYnabClientFactory(engine=engine).create_client(budgetname='Test Budget',
                                                                     connection=MockConnection,
                                                                     new=True,
                                                                     sync=False)
            client.budgetClient.update_from_changed_entitydict_bulk(data)
            updated_memos = [tr.memo for tr in client.budget.be_transactions]
            self.assertItemsEqual(memos, updated_memos)

        result1 = timeit.timeit(case1, number=3)

        result2 = timeit.timeit(case2, number=3)

        pass
