import unittest

from pynYNAB.ClientFactory import nYnabClientFactory
from tests.common_mock import MockConnection

connection = MockConnection()
factory = nYnabClientFactory('sqlite://')


class MockConnection(object):
    def __init__(self,id):
        self.id = id


class Args(object):
    budget_name = 'Test Budget'

    def __init__(self, user_id):
        self.connection = MockConnection(user_id)


class TestPersist(unittest.TestCase):
    def test_client_persist(self):
        cl1 = factory.create_client(Args('12345'), sync=False)
        cl2 = factory.create_client(Args('12345'), sync=False)
        self.assertEqual(cl1,cl2)
        cl3 = factory.create_client(Args('54231'), sync=False)
        self.assertNotEqual(cl1, cl3)