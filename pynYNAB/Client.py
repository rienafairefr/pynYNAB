import logging
from functools import wraps

from pynYNAB.Entity import obj_from_dict
from pynYNAB.connection import NYnabConnectionError, nYnabConnection
from pynYNAB.roots import Budget, Catalog
from pynYNAB.schema.budget import Payee, Transaction
from pynYNAB.schema.catalog import BudgetVersion
from pynYNAB.scripts.config import get_logger
from pynYNAB.utils import chunk

logger = logging.getLogger('pynYNAB')


def clientfromargs(args, reset=False):
    return nYnabClient.from_obj(args,reset)


class BudgetNotFound(Exception):
    pass


class nYnabClient(object):
    def __init__(self, nynabconnection, budget_name):
        self.delta_device_knowledge = 0
        self.budget_version_id = None
        self.logger = get_logger()
        if budget_name is None:
            logger.error('No budget name was provided')
            exit(-1)
        self.budget_name = budget_name
        self.connection = nynabconnection
        self.budget_name = budget_name
        self.catalog = Catalog()
        self.budget = Budget()
        self.budget_version = BudgetVersion()

        self.current_device_knowledge = {}
        self.device_knowledge_of_server = {}

        self.first = True
        self.sync()

    @staticmethod
    def from_obj(args, reset=False):
        connection = nYnabConnection(args.email, args.password)
        try:
            client = nYnabClient(connection, budget_name=args.budgetname)
            if reset:
                # deletes the budget
                client.delete_budget(args.budgetname)
                client.create_budget(args.budgetname)
                client.select_budget(args.budgetname)
            return client
        except BudgetNotFound:
            print('No budget by the name %s found in nYNAB' % args.budgetname)
            exit(-1)

    def getinitialdata(self):
        try:
            getinitialdata = self.connection.dorequest({"device_info": {'id': self.connection.id}},
                                                       'getInitialUserData')
            self.budget.update_from_changed_entities(getinitialdata['budget'])
            self.budget_version.update_from_dict(getinitialdata['budget_version'])
            pass
        except NYnabConnectionError:
            pass

    def sync(self):
        # ending-starting represents the number of modifications that have been done to the data ?
        self.logger.debug('Catalog sync')
        if self.first:
            self.first = False
            self.sync_obj(self.catalog, 'syncCatalogData', knowledge=False)
            for catalogbudget in self.catalog.ce_budgets:
                if catalogbudget.budget_name == self.budget_name:
                    for budget_version in self.catalog.ce_budget_versions:
                        if budget_version.budget_id == catalogbudget.id:
                            self.budget_version_id = budget_version.id
            self.sync_obj(self.budget, 'syncBudgetData', knowledge=False,extra=dict(calculated_entities_included=False,budget_version_id=self.budget_version_id))
        if self.budget_version_id is None and self.budget_name is not None:
            raise BudgetNotFound()
        else:
            catalog_changed_entities = self.catalog.get_changed_entities()
            budget_changed_entities = self.budget.get_changed_entities()

            if any(catalog_changed_entities) or any(budget_changed_entities):
                self.delta_device_knowledge = 1
            else:
                self.delta_device_knowledge = 0

            self.sync_obj(self.catalog, 'syncCatalogData',extra=dict(user_id="fbec95c7-9fd2-415e-9365-7c4a8e613a49"))
            self.sync_obj(self.budget, 'syncBudgetData',extra=dict(calculated_entities_included=False,budget_version_id=self.budget_version_id))

    def update_from_sync_data(self,obj,sync_data):
        for namefield in obj.ListFields:
            getattr(obj, namefield).changed = []
        changed_entities = {}
        for name, value in sync_data['changed_entities'].items():
            if isinstance(value, list):
                for entityDict in value:
                    new_obj = obj_from_dict(obj.ListFields[name].type, entityDict)
                    try:
                        changed_entities[name].append(new_obj)
                    except KeyError:
                        changed_entities[name] = [new_obj]
            else:
                changed_entities[name] = obj.AllFields[name].posttreat(value)
        obj.update_from_changed_entities(changed_entities)

    def sync_obj(self, obj, opname,knowledge=True,extra=None):
        if extra is None:
            extra = {}
        if opname not in self.current_device_knowledge:
            self.current_device_knowledge[opname] = 0
        if opname not in self.device_knowledge_of_server:
            self.device_knowledge_of_server[opname] = 0
        if knowledge:
            changed_entities = obj.get_changed_entities()
        else:
            changed_entities={}
            # sync with disregard for knowledge, start from 0
        request_data = dict(starting_device_knowledge=self.current_device_knowledge[opname],
                                ending_device_knowledge=self.current_device_knowledge[opname],
                                device_knowledge_of_server=self.device_knowledge_of_server[opname],
                                changed_entities={})
        request_data.update(extra)

        sync_data = self.connection.dorequest(request_data, opname)
        self.update_from_sync_data(obj,sync_data)

        server_knowledge_of_device = sync_data['server_knowledge_of_device']
        current_server_knowledge = sync_data['current_server_knowledge']

        change = current_server_knowledge - self.device_knowledge_of_server[opname]
        if change > 0:
            self.logger.debug('Server knowledge has gone up by ' + str(
                change) + '. We should be getting back some entities from the server')
        if self.current_device_knowledge[opname] < server_knowledge_of_device:
            if self.current_device_knowledge[opname] != 0:
                self.logger.error('The server knows more about this device than we know about ourselves')
            self.current_device_knowledge[opname] = server_knowledge_of_device
        self.device_knowledge_of_server[opname] = current_server_knowledge

        self.logger.debug('current_device_knowledge %s' % self.current_device_knowledge[opname])
        self.logger.debug('device_knowledge_of_server %s' % self.device_knowledge_of_server[opname])

    def operation(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            fn(self, *args, **kwargs)
            self.sync()

        return wrapped

    @operation
    def add_account(self, account, balance, balance_date):
        payee = Payee(
            entities_account_id=account.id,
            enabled=True,
            auto_fill_subcategory_enabled=True,
            auto_fill_memo_enabled=False,
            auto_fill_amount_enabled=False,
            rename_on_import_enabled=False,
            name="Transfer : %s" % account.account_name
        )
        immediateincomeid = next(
            s.id for s in self.budget.be_subcategories if s.internal_name == 'Category/__ImmediateIncome__')
        startingbalanceid = next(p.id for p in self.budget.be_payees if p.internal_name == 'StartingBalancePayee')

        transaction = Transaction(
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

    def add_transactions(self, transaction_list):
        for chunkelement in chunk(transaction_list, 50):
            self._add_transactions(chunkelement)

    @operation
    def _add_transactions(self, transaction_list):
        for transaction in transaction_list:
            self.budget.be_transactions.append(transaction)

    @operation
    def delete_transaction(self, transaction):
        self.budget.be_transactions.delete(transaction)

    def select_account_ui(self, create=False):
        accounts = list(self.budget.be_accounts)

        iaccount = 0
        if create:
            print('#0 ###CREATE')
            iaccount = 1

        for account in accounts:
            print('#%d %s' % (iaccount, account.account_name))
            iaccount += 1
        if create:
            accounts = [None] + accounts

        while True:
            accountnumber = input('Which account? ')
            try:
                accountnumber = int(accountnumber)
                if 0 <= accountnumber <= len(accounts) - 1:
                    break
            except ValueError:
                pass
            print('Please enter a number between %d and %d' % (0, len(accounts) - 1))
            return accounts[accountnumber]

    @operation
    def delete_budget(self, budget_name):
        for budget in self.catalog.ce_budgets:
            if budget.budget_name == budget_name:
                budget.is_tombstone = True
                self.catalog.ce_budgets.modify(budget)

    def select_budget(self, budget_name):
        self.logger.debug('Catalog sync')
        self.catalog.sync(self.connection, 'syncCatalogData')
        for budget_version in self.catalog.ce_budget_versions:
            budget = self.catalog.ce_budgets.get(budget_version.budget_id)
            if budget.budget_name == budget_name:
                self.budget.budget_version_id = budget_version.id
                self.logger.debug('Budget sync')
                self.sync()
                break

    def create_budget(self, budget_name):
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

    @operation
    def clean_transactions(self):
        for transaction in self.budget.be_transactions:
            self.budget.be_transactions.delete(transaction)
        for subtransaction in self.budget.be_subtransactions:
            self.budget.be_subtransactions.delete(subtransaction)

    @operation
    def clean_budget(self):
        self.clean_transactions()
        for sub_category in [sub_category for sub_category in self.budget.be_subcategories if
                             sub_category.internal_name is None]:
            self.budget.be_subcategories.delete(sub_category)
        for mastercategory in [mastercategory for mastercategory in self.budget.be_master_categories if
                               mastercategory.deletable]:
            self.budget.be_master_categories.delete(mastercategory)
        self.clean_transactions()
        for payee in [payee for payee in self.budget.be_payees if payee.internal_name is None]:
            self.budget.be_payees.delete(payee)
        for account in self.budget.be_accounts:
            self.budget.be_accounts.delete(account)
