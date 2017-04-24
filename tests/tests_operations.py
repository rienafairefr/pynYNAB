import json

from pynYNAB.Client import nYnabClient, nYnabClientFactory, Catalog, Budget
from pynYNAB.exceptions import NoBudgetNameException
from pynYNAB.schema.catalog import BudgetVersion
from tests.common_mock import TestCommonMock, MockClientData, mockSession, MockConnection

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


class Args(object):
    budgetname = 'budgetname'
    nynabconnection = MockConnection()
    engine = 'sqlite://'
    email = 'email'
    password = 'password'


class TestOperations(TestCommonMock):
    def test_create_budget(self):
        def dorequest(request_dic, opname):
            d={'changed_entities':{}}
            if opname == 'CreateNewBudget':
                self.assertEqual(opname, opname)
                self.assertEqual(request_dic['currency_format'], json.dumps(currency_format))
                self.assertEqual(request_dic['date_format'], json.dumps(date_format))
                return d
            if opname == 'syncCatalogData':
                d.update({'changed_entities':{k:[] for k in Catalog().listfields.keys()}})
            if opname == 'syncBudgetData':
                d.update({k: [] for k in Budget().listfields.keys()})
            d.update(dict(server_knowledge_of_device=0, current_server_knowledge=0))
            return d

        mock = MockConnection()
        mock.dorequest=dorequest
        arg = Args()
        arg.nynabconnection = mock

        self.client = nYnabClientFactory.from_obj(arg)
        self.client.create_budget(budget_name='New Budget')

    def test_client_nobudget(self):
        arg = Args()
        arg.budgetname = None
        self.assertRaises(NoBudgetNameException,lambda:nYnabClientFactory.from_obj(arg))

    def test_select_budget(self):
        data = MockClientData()
        data.budget_name = 'Testbudget'
        self.client = nYnabClient(Args())
        budget_version1 = BudgetVersion(version_name='TestBudget')
        budget_version2 = BudgetVersion(version_name='NewTestBudget')
        self.client.catalog.ce_budget_versions= [budget_version1,budget_version2]

        self.client.select_budget(budget_name='NewTestBudget')
        self.assertEqual(budget_version2.id,self.client.budget_version_id)

    def test_create_client(self):
        client = nYnabClientFactory.from_obj(Args(),sync=False)
        self.assertEqual(Args.nynabconnection,client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual(Args.engine, str(client.session.bind.url))

    def test_create_client_nynabconnectionparameter(self):
        class Args(object):
            nynabconnection = MockConnection()
            budgetname = 'budgetname'
            email = 'email'
            password = 'password'

        client = nYnabClientFactory.from_obj(Args(), sync=False)
        self.assertEqual(Args.nynabconnection, client.connection)
        self.assertEqual(Args.budgetname, client.budget_name)
        self.assertEqual('sqlite://', str(client.session.bind.url))
