import unittest

from pynYNAB.ClientFactory import nYnabClientFactory
from .common_mock import MockConnection

connection = MockConnection()
factory = nYnabClientFactory('sqlite://')


class MockConnection(object):
    def __init__(self,id):
        self.id = id


class TestPersist(unittest.TestCase):
    def test_client_persist(self):
        cl1 = factory.create_client(budget_name='Test Budget', connection=MockConnection('12345'), sync=False)
        cl2 = factory.create_client(budget_name='Test Budget', connection=MockConnection('12345'), sync=False)
        self.assertEqual(cl1,cl2)
        cl3 = factory.create_client(budget_name='Test Budget', connection=MockConnection('54231'), sync=False)
        self.assertNotEqual(cl1, cl3)