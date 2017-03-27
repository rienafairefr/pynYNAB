import json

import atexit

from pynYNAB.Client import nYnabClient, NoBudgetNameException, BudgetNotFound
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


class TestOperations(TestCommonMock):
    def test_create_budget(self):
        class MockConnection(object):
            def __init__(self):
                self.user_id = '1234'

            def dorequest(s, request_dic, opname):
                self.assertEqual(opname, opname)
                self.assertEqual(request_dic['currency_format'], json.dumps(currency_format))
                self.assertEqual(request_dic['date_format'], json.dumps(date_format))

        self.client = nYnabClient(budgetname='TestBudget', nynabconnection=MockConnection())
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
            nynabconnection='nynabconnection'
            budgetname='budgetname'
            engine='sqlite:///:memory:'
        client = nYnabClient.from_obj(Args(),sync=False)
        self.assertEqual(Args.nynabconnection,client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual(Args.engine, str(client.session.bind.url))

    def test_create_client_nynabconnectionparameter(self):
        class Args(object):
            nynabconnection = 'nynabconnection'
            budgetname = 'budgetname'

        client = nYnabClient.from_obj(Args(), sync=False)
        self.assertEqual(Args.nynabconnection, client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual('sqlite://', str(client.session.bind.url))

    def test_create_client_auth_parameters_passed_to_connection(self):
        class Args(object):
            email = 'email'
            password = 'password'
            budgetname = 'budgetname'

        client = nYnabClient.from_obj(Args(), sync=False, init_connection=False)
        self.assertEqual(Args.email, client.connection.email)
        self.assertEqual(Args.password, client.connection.password)
        self.assertEqual(Args.budgetname, client.budget_name)
