import unittest

from pynYNAB.ClientFactory import nYnabClientFactory
from tests.common_mock import MockConnection

connection = MockConnection()
factory = nYnabClientFactory('sqlite://')


class Args(object):
    nynabconnection = MockConnection()
    budget_name = 'Test Budget'


class TestPersist(unittest.TestCase):
    def test_client_persist(self):
        cl1 = factory.create_client(Args, sync=False)
        cl2 = factory.create_client(Args, sync=False)