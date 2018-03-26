import unittest

from pynYNAB.schema import BudgetVersion, MasterCategory, SubCategory, Payee
from tests.common_mock import factory, MockConnection


class TestCommonMock(unittest.TestCase):
    def setUp(self):
        self.client = factory.create_client(budget_name='TestBudget',
                                            connection=MockConnection(),
                                            sync=False)

        session = self.client.session

        budget_version = BudgetVersion(version_name='TestBudget')
        master_category = MasterCategory(name='master')
        subcategory = SubCategory(name='Immediate Income',
                                  internal_name='Category/__ImmediateIncome__',
                                  entities_master_category=master_category)
        payee = Payee(name='Starting Balance Payee', internal_name='StartingBalancePayee')
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