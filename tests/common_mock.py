import unittest

import mock
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from pynYNAB.Client import nYnabClient, nYnabClientFactory
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema import Base, nYnabClientData
from pynYNAB.schema.budget import SubCategory, Payee, MasterCategory
from pynYNAB.schema.catalog import BudgetVersion
from pynYNAB.schema.roots import Catalog, Budget


class MockConnection(object):
    def __init__(self):
        self.user_id = '1234'
        self.catalog = Catalog()
        self.budget = Budget()

    def dorequest(self, request_dic, opname):
        if opname == 'syncCatalogData':
            return {'changed_entities':{k:[] for k in self.catalog.listfields},'server_knowledge_of_device':0,'current_server_knowledge':123}
        if opname == 'syncBudgetData':
            return {'changed_entities':{k:[] for k in self.budget.listfields},'server_knowledge_of_device':0,'current_server_knowledge':123}

    def init_session(self):
        pass



class MockClientData(object):
    nynabconnection = MockConnection()
    budget_name = 'budgetname'
    budget_version_id = '12345'
    engine = 'sqlite:///:memory:'
    email = 'email'
    password = 'password'
    catalog = Catalog()
    budget = Budget()
    starting_device_knowledge = 0
    ending_device_knowledge = 0
    user_id = 'user_id'

class Args(object):
    budgetname = 'budgetname'
    nynabconnection = MockConnection()
    engine = 'sqlite://'
    email = 'email'
    password = 'password'

mockSession=mock.Mock(spec=Session)

class TestCommonMock(unittest.TestCase):
    def setUp(self):
        self.client = nYnabClientFactory.from_obj(Args(),sync=False)

        session = self.client.session

        budget_version = BudgetVersion(version_name='TestBudget')
        master_category = MasterCategory(name='master')
        subcategory = SubCategory(name='Immediate Income',
                                  internal_name='Category/__ImmediateIncome__',
                                  entities_master_category=master_category)
        payee = Payee(name='Starting Balance Payee',internal_name='StartingBalancePayee')
        session.add(master_category)
        session.add(subcategory)
        session.add(payee)

        self.client.catalog.ce_budget_versions.append(budget_version)
        self.client.budget.be_master_categories.append(master_category)
        self.client.budget.be_subcategories.append(subcategory)
        self.client.budget.be_payees.append(payee)
        session.commit()
        self.client.budget.clear_changed_entities()
        self.client.catalog.clear_changed_entities()

        self.client.budgetClient.device_knowledge_of_server = 0
        self.client.catalogClient.device_knowledge_of_server = 0

        self.client.budgetClient.current_device_knowledge = 0
        self.client.catalogClient.current_device_knowledge = 0

        pass
