import json

from pynYNAB.Client import nYnabClient
from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.exceptions import NoBudgetNameException
from pynYNAB.schema.catalog import BudgetVersion
from .common_mock import TestCommonMock

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


class MockConnection2(object):
    id='12345'

factory = nYnabClientFactory('sqlite://')


class TestOperations(TestCommonMock):
    def test_create_budget(self):
        class MockConnection2(object):
            def dorequest(this,request_dic, opname):
                self.assertEqual(opname, opname)
                self.assertEqual(request_dic['currency_format'], json.dumps(currency_format))
                self.assertEqual(request_dic['date_format'], json.dumps(date_format))
            user_id = '1234'
            id = '1234'

        self.client = factory.create_client(budget_name='', connection=MockConnection2(), sync=False)
        self.client.create_budget(budget_name='New Budget')

    def test_client_nobudget(self):
        def create_client_no_budget():
            client = nYnabClient()
        self.assertRaises(NoBudgetNameException, create_client_no_budget)

    def test_select_budget(self):
        client = factory.create_client(budget_name='',connection=MockConnection2(), sync=False)
        budget_version1 = BudgetVersion(version_name='TestBudget')
        budget_version2 = BudgetVersion(version_name='NewTestBudget')
        client.catalog.budget_versions= [budget_version1, budget_version2]

        client.select_budget(budget_name='NewTestBudget')
        self.assertEqual(budget_version2.id, client.budget_version_id)

    def test_create_client(self):
        nynabconnection = MockConnection2()
        budgetname = 'budgetname'
        client = factory.create_client(connection=nynabconnection, budget_name=budgetname, sync=False)
        self.assertEqual(nynabconnection,client.connection)
        self.assertEqual(nynabconnection, client.catalogClient.connection)
        self.assertEqual(nynabconnection, client.budgetClient.connection)
        self.assertEqual(budgetname, client.budget_name)

    def test_create_client_nynabconnectionparameter(self):
        nynabconnection = MockConnection2()
        budgetname = 'budgetname'

        client = factory.create_client(connection= nynabconnection, budget_name=budgetname, sync=False)
        self.assertEqual(nynabconnection, client.connection)
        self.assertEqual(budgetname, client.budget_name)
        self.assertEqual('sqlite://', str(client.session.bind.url))
