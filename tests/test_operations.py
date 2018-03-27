import json

import pytest

from pynYNAB.Client import nYnabClient
from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.exceptions import NoBudgetNameException
from pynYNAB.schema.catalog import BudgetVersion


class MockConnection2(object):
    id = '12345'


@pytest.fixture
def factory():
    return nYnabClientFactory('sqlite://')


@pytest.fixture
def connection():
    return MockConnection2()


@pytest.fixture
def client(factory, connection):
    return factory.create_client(budget_name='budget_name', connection=connection, sync=False)


def test_create_budget(factory):
    currency_format = dict(
        iso_code='USD',
        example_format='123,456.78',
        decimal_digits=2,
        decimal_separator='.',
        symbol_first=True,
        group_separator=',',
        currency_symbol='$',
        display_symbol=True
    )
    date_format = dict(
        format='MM/DD/YYYY'
    )

    class MockConnection(object):
        def dorequest(this, request_dic, opname):
            assert opname == opname
            assert request_dic['currency_format'] == json.dumps(currency_format)
            assert request_dic['date_format'] == json.dumps(date_format)

        user_id = '1234'
        id = '1234'

    client = factory.create_client(budget_name='budget_name', connection=MockConnection(), sync=False)

    client.create_budget(budget_name='New Budget')


def test_client_nobudget():
    def create_client_no_budget():
        nYnabClient()

    pytest.raises(NoBudgetNameException, create_client_no_budget)


def test_select_budget(client):
    budget_version1 = BudgetVersion(version_name='TestBudget')
    budget_version2 = BudgetVersion(version_name='NewTestBudget')
    client.catalog.ce_budget_versions = [budget_version1, budget_version2]

    client.select_budget(budget_name='NewTestBudget')
    assert budget_version2.id == client.budget_version_id


def test_create_client(client, connection):
    assert connection == client.connection
    assert connection == client.catalogClient.connection
    assert connection == client.budgetClient.connection
    assert 'budget_name' == client.budget_name
    assert 'sqlite://' == str(client.session.bind.url)
