import unittest

from pynYNAB.Client import nYnabClient
from pynYNAB.schema.budget import SubCategory, Payee, MasterCategory


class TestCommonMock(unittest.TestCase):
    def setUp(self):
        self.client = nYnabClient(budgetname='')
        master_category=MasterCategory(name='master')
        self.client.budget.be_master_categories.append(master_category)
        self.client.budget.be_subcategories.append(SubCategory(name ='Immediate Income',
            internal_name='Category/__ImmediateIncome__',
                                                               entities_master_category=master_category))
        self.client.budget.be_payees.append(Payee(name='Starting Balance Payee',internal_name='StartingBalancePayee'))
