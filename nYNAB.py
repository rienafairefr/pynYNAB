import copy
import os
import pickle

from Entity import ListofEntities
from NYnabConnection import NYnabConnectionError
from budget import  TransactionGroup
from catalog import BudgetVersion
from config import appdir
from roots import Budget, Catalog


class NYnab(object):
    def __init__(self, nynabconnection, reload=False):
        self.connection=nynabconnection
        self.catalog=Catalog()
        self.budget=Budget()
        self.budget_version=BudgetVersion()
        self.getinitialdata()
        self.budget.budget_version_id=self.budget_version.id
        if reload:
            self.sync()
        else:
            try:
                self.load()
            except:
                self.sync()

    catalogpath=os.path.join(appdir.user_data_dir,'catalog')
    budgetpath=os.path.join(appdir.user_data_dir,'budget')

    def getinitialdata(self):
        try:
            getinitialdata=self.connection.dorequest({"device_info": {'id':self.connection.id}}, 'getInitialUserData')
            self.budget.update_from_changed_entities(getinitialdata['budget'])
            self.budget_version.update_from_dict(getinitialdata['budget_version'])
            pass
        except NYnabConnectionError:
            pass

    def sync(self):
        # ending-starting represents the number of modifications that have been done to the data ?
        self.catalog.sync(self.connection,'syncCatalogData')
        self.budget.sync(self.connection,'syncBudgetData')


    def load(self):
        with open(self.catalogpath,'r') as file:
            self.catalog=pickle.load(file)
        with open(self.budgetpath,'r') as file:
            self.budgetsdict=pickle.load(file)

    def save(self):
        with open(self.catalogpath,'w') as file:
            pickle.dump(self.catalog,file)
        with open(self.budgetpath,'w') as file:
            pickle.dump(self.budgetsdict,file)
