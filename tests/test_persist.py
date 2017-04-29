import unittest

from pynYNAB.ClientFactory import nYnabClientFactory
from tests.common_mock import MockConnection

connection = MockConnection()
factory = nYnabClientFactory('sqlite://')


class Args(object):
    email = 'email'
    password = 'password'
    budgetname = 'budgetname'
    nynabconnection = MockConnection()
    budget_name = 'Test Budget'


class TestPersist(unittest.TestCase):
    def test_client_persist(self):
        args = Args()

        cl1 = factory.create_client(args, sync=False)
        cl2 = factory.create_client(args, sync=False)