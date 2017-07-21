import json
import unittest

from sqlalchemy import create_engine

from pynYNAB.ClientFactory import nYnabClientFactory


class TestSyncMock(unittest.TestCase):
    def test_sync_mock(self):
        class MockConnection(object):
            user_id='1'

            def dorequest(self, request_data, opname):
                with open(opname+'.json','r') as f:
                    data = json.load(f)
                    return data
        engine= create_engine('sqlite:///:memory:',echo=True)

        client = nYnabClientFactory(engine=engine).create_client(budgetname='Test Budget',
                                                                 connection = MockConnection(),
                                                                 sync=True)


    def test_update_obj(self):
        pass

