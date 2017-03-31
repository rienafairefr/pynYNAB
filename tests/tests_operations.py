import json

import atexit
try:
    from unittest.mock import Mock
    from unittest import mock
except ImportError:
    from mock import Mock

from pynYNAB.Client import nYnabClient, NoBudgetNameException, BudgetNotFound
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.catalog import BudgetVersion, User
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


class TestOperations(TestCommonMock):
    def test_create_budget(self):
        def dorequest( request_dic, opname):
            self.assertEqual(opname, opname)
            self.assertEqual(request_dic['currency_format'], json.dumps(currency_format))
            self.assertEqual(request_dic['date_format'], json.dumps(date_format))

        mock = MockConnection()
        mock.dorequest=dorequest

        self.client = nYnabClient(budgetname='TestBudget', nynabconnection=mock)
        self.client.create_budget(budget_name='New Budget')

    def test_client_nobudget(self):
        self.assertRaises(NoBudgetNameException,lambda:nYnabClient())

    def test_select_budget(self):
        self.client = nYnabClient(budgetname='TestBudget')
        budget_version1 = BudgetVersion(version_name='TestBudget')
        budget_version2 = BudgetVersion(version_name='NewTestBudget')
        self.client.catalog.ce_budget_versions= [budget_version1,budget_version2]

        self.client.select_budget(budget_name='NewTestBudget')
        self.assertEqual(budget_version2.id,self.client.budget_version_id)

    def test_create_client(self):
        class Args(object):
            nynabconnection=MockConnection()
            budgetname='budgetname'
            engine='sqlite:///:memory:'
        client = nYnabClient.from_obj(Args(),sync=False)
        self.assertEqual(Args.nynabconnection,client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual(Args.engine, str(client.session.bind.url))

    def test_create_client_nynabconnectionparameter(self):
        class Args(object):
            nynabconnection = MockConnection()
            budgetname = 'budgetname'

        client = nYnabClient.from_obj(Args(), sync=False)
        self.assertEqual(Args.nynabconnection, client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual('sqlite://', str(client.session.bind.url))
