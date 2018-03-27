from pynYNAB.ClientFactory import nYnabClientFactory
from .common_mock import MockConnection

connection = MockConnection()
factory = nYnabClientFactory('sqlite://')


class MockConnection(object):
    def __init__(self, id):
        self.id = id


def test_client_persist():
    def get_cl(id):
        return factory.create_client(budget_name='Test Budget', connection=MockConnection(id), sync=False)
    cl1 = get_cl('12345')
    cl2 = get_cl('12345')
    assert cl1 == cl2
    cl3 = get_cl('54321')
    assert cl1 != cl3
