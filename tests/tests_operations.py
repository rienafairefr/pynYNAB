import json

from pynYNAB.exceptions import NoBudgetNameException

try:
    from unittest.mock import Mock
    from unittest import mock
except ImportError:
    from mock import Mock,mock

from pynYNAB.Client import nYnabClient
from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.catalog import BudgetVersion
from tests.common_mock import TestCommonMock


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

MockConnection = Mock(spec=nYnabConnection)

factory = nYnabClientFactory('sqlite://')

class TestOperations(TestCommonMock):
    def test_create_budget(self):
        def dorequest( request_dic, opname):
            self.assertEqual(opname, opname)
            self.assertEqual(request_dic['currency_format'], json.dumps(currency_format))
            self.assertEqual(request_dic['date_format'], json.dumps(date_format))

        mock_connection = MockConnection()
        mock_connection.dorequest=dorequest

        class Args(object):
            email = 'email'
            password = 'password'
            nynabconnection = mock_connection
            budgetname = 'Test Budget'


        self.client = factory.create_client(Args(), sync=False)
        self.client.create_budget(budget_name='New Budget')

    def test_client_nobudget(self):
        def create_client_no_budget():
            client = nYnabClient()
        self.assertRaises(NoBudgetNameException, create_client_no_budget)

    def test_select_budget(self):
        class Args(object):
            email = 'email'
            password = 'password'
            budgetname = 'budgetname'
            nynabconnection = MockConnection()
            budget_name = 'Test Budget'

        client = factory.create_client(Args(), sync=False)
        budget_version1 = BudgetVersion(version_name='TestBudget')
        budget_version2 = BudgetVersion(version_name='NewTestBudget')
        client.catalog.ce_budget_versions= [budget_version1, budget_version2]

        client.select_budget(budget_name='NewTestBudget')
        self.assertEqual(budget_version2.id, client.budget_version_id)

    def test_create_client(self):
        class Args(object):
            nynabconnection = MockConnection()
            budgetname = 'budgetname'
            email = 'email'
            password = 'password'
        client = factory.create_client(Args(), sync=False)
        self.assertEqual(Args.nynabconnection,client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)

    def test_create_client_nynabconnectionparameter(self):
        class Args(object):
            nynabconnection = MockConnection()
            budgetname = 'budgetname'
            email = 'email'
            password = 'password'

        client = factory.create_client(Args(), sync=False)
        self.assertEqual(Args.nynabconnection, client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual('sqlite://', str(client.session.bind.url))
