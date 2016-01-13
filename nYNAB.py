import copy
import os
import pickle
from budget import BudgetBudget
from catalog import Catalog
from config import appdir

class nYNAB(object):
    def __init__(self,nynabconnexion,reload=False):
        self.ynab=nynabconnexion
        self.previouscatalog=Catalog()
        self.catalog=Catalog()
        self.previousbudgetsdict={}
        self.budgetsdict={}
        if reload:
            self.sync()
        else:
            try:
                self.load()
            except:
                self.sync()


    catalogpath=os.path.join(appdir.user_data_dir,'catalog')
    budgetpath=os.path.join(appdir.user_data_dir,'budget')

    def sync(self):
        # ending-starting represents the number of modifications that have been done to the data ?
        self.previouscatalog=copy.copy(self.catalog)
        changed_entities=self.catalog.get_changed_entities(self.previouscatalog)
        syncCatalogData=self.ynab.dorequest({"starting_device_knowledge":self.catalog.knowledge,
                                             "ending_device_knowledge":self.catalog.current_knowledge,
                                             "device_knowledge_of_server":self.catalog.device_knowledge_of_server,
                                             "changed_entities":changed_entities},'syncCatalogData')
        self.catalog.update_from_changed_entities(syncCatalogData['changed_entities'])
        self.catalog.server_knowledge_of_device=syncCatalogData['server_knowledge_of_device']
        self.catalog.device_knowledge_of_server=syncCatalogData['current_server_knowledge']

        self.previousbudgetdict=copy.copy(self.budgetsdict)
        for budget_version in self.catalog.ce_budget_versions:
            try:
                budget=self.budgetsdict[budget_version.id]
                previousbudget=self.previousbudgetsdict[budget_version.id]
            except KeyError:
                budget=BudgetBudget()
                previousbudget=BudgetBudget()
            changed_entities=budget.get_changed_entities(previousbudget)
            syncBudget=self.ynab.dorequest({"budget_version_id":budget_version.id,
                                            "starting_device_knowledge":previousbudget.knowledge,
                                            "ending_device_knowledge":previousbudget.current_knowledge,
                                            "device_knowledge_of_server":previousbudget.device_knowledge_of_server,
                                            "calculated_entities_included":False,
                                            "changed_entities":changed_entities},'syncBudgetData')

            budget.update_from_changed_entities(syncBudget['changed_entities'])
            budget.server_knowledge_of_device=syncBudget['server_knowledge_of_device']
            budget.device_knowledge_of_server=syncBudget['current_server_knowledge']

            self.budgetsdict[budget_version.id]=budget
            self.previousbudgetsdict[budget_version.id]=budget

        self.budgets=self.budgetsdict.values()

    def load(self):
        with open(self.catalogpath,'r') as file:
            self.catalog=pickle.load(file)
        with open(self.budgetpath,'r') as file:
            self.budget=pickle.load(file)

    def save(self):
        with open(self.catalogpath,'w') as file:
            pickle.dump(self.catalog,file)
        with open(self.budgetpath,'w') as file:
            pickle.dump(self.catalog,file)
