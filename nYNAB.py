import copy
import os
import pickle
from functools import wraps

from Entity import ListofEntities
from NYnabConnection import NYnabConnectionError
from budget import  TransactionGroup, Payee, Transaction
from catalog import BudgetVersion
from config import appdir
from roots import Budget, Catalog

class BudgetNotFound(Exception):
    pass

class nYnab(object):
    def  __init__(self, nynabconnection, budget_name=None, reload=False):
        self.connection=nynabconnection
        self.budget_name=budget_name
        self.do_init(reload)

    def do_init(self,reload=False):
        self.catalog=Catalog()
        self.budget=Budget()
        self.budget_version=BudgetVersion()
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
        if self.budget.budget_version_id is None:
            for catalogbudget in self.catalog.ce_budgets:
                if catalogbudget.budget_name == self.budget_name and not catalogbudget.is_tombstone:
                    for budget_version in self.catalog.ce_budget_versions:
                        if budget_version.budget_id == catalogbudget.id:
                            self.budget.budget_version_id=budget_version.id
        if self.budget.budget_version_id is None:
            raise BudgetNotFound()
        else:
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

    def operation(fn):
        @wraps(fn)
        def wrapped(self,*args,**kwargs):
            fn(self,*args,**kwargs)
            self.sync()
        return wrapped

    @operation
    def add_account(self, account, balance, balance_date):
        payee=Payee(
            entities_account_id=account.id,
            enabled=True,
            auto_fill_subcategory_enabled=True,
            auto_fill_memo_enabled=False,
            auto_fill_amount_enabled=False,
            rename_on_import_enabled=False,
            name="Transfer : %s" % account.account_name
        )
        immediateincomeid=next(s.id for s in self.budget.be_subcategories if s.internal_name == 'Category/__ImmediateIncome__')
        startingbalanceid=next(p.id for p in self.budget.be_payees if p.internal_name == 'StartingBalancePayee')

        transaction=Transaction(
            accepted=True,
            amount=balance,
            entities_subcategory_id=immediateincomeid,
            cash_amount=0,
            cleared='Cleared',
            date=balance_date,
            entities_account_id=account.id,
            credit_amount=0,
            entities_payee_id=startingbalanceid,
            is_tombstone=False
        )

        self.budget.be_accounts.append(account)
        self.budget.be_payees.append(payee)
        self.budget.be_transactions.append(transaction)

    @operation
    def delete_account(self, account):
        self.budget.be_accounts.delete(account)

    @operation
    def add_transaction(self, transaction):
        self.budget.be_transactions.append(transaction)

    @operation
    def add_transactions(self,transaction_list):
        for transaction in transaction_list:
            self.budget.be_transactions.append(transaction)

    @operation
    def delete_transaction(self, transaction):
        self.budget.be_transactions.delete(transaction)

    def createbudget(self, budget_name):
        import json
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
        self.connection.dorequest(opname='CreateNewBudget',
                                  request_dic={
                                      "budget_name": budget_name,
                                      "currency_format": json.dumps(currency_format),
                                      "date_format": json.dumps(date_format)
                                  })
    def clean_budget(self):
        for sub_category in [sub_category for sub_category in self.budget.be_subcategories if sub_category.internal_name is None]:
            self.budget.be_subcategories.delete(sub_category)
        for mastercategory in [mastercategory for mastercategory in self.budget.be_master_categories if mastercategory.deletable]:
            self.budget.be_master_categories.delete(mastercategory)
        for transaction in self.budget.be_transactions:
            self.budget.be_transactions.delete(transaction)
        for payee in [payee for payee in self.budget.be_payees if payee.internal_name is None]:
            self.budget.be_payees.delete(payee)
        for account in self.budget.be_accounts:
            self.budget.be_accounts.delete(account)
        self.sync()
