import logging
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.ObjClient import RootObjClient
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.Entity import Base
from pynYNAB.schema.budget import Payee, Transaction
from pynYNAB.schema.catalog import BudgetVersion
from pynYNAB.schema.roots import Budget
from pynYNAB.schema.roots import Catalog
from pynYNAB.utils import chunk

LOG = logging.getLogger(__name__)


class BudgetNotFound(Exception):
    pass


# noinspection PyPep8Naming
class WrongPushException(Exception):
    def __init__(self, expected_delta, delta):
        self.expected_delta = expected_delta
        self.delta = delta

    string = 'tried to push a changed_entities with %d entities while we expected %d entities'

    @property
    def msg(self):
        return self.string % (self.delta, self.expected_delta)


def operation(expected_delta):
    def operation_decorator(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            fn(self, *args, **kwargs)
            self.logger.debug('push after '+fn.__name__)
            self.push(expected_delta)
        return wrapped
    return operation_decorator


class nYnabClient(object):
    def __init__(self, **kwargs):
        self.server_entities = {}
        self.budget_version_id = None
        self.logger = kwargs.get('logger', None)

        self.budget_name = kwargs.get('budgetname', None)
        if self.budget_name is None:
            logger.error('No budget name was provided')
            exit(-1)
        self.connection = kwargs.get('nynabconnection', None)
        self.catalog = Catalog()
        self.budget = Budget()
        self.budget_version = BudgetVersion()

        self.current_device_knowledge = {}
        self.device_knowledge_of_server = {}
        self.starting_device_knowledge = 0
        self.ending_device_knowledge = 0

        engine = kwargs.get('engine', create_engine('sqlite://'))

        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

        self.session = self.Session()
        self.session.add(self.catalog)
        self.session.add(self.budget)
        self.session.commit()

        self.online = self.connection is not None
        self.catalogClient = RootObjClient(self.catalog, self, 'syncCatalogData')
        self.budgetClient = RootObjClient(self.budget, self, 'syncBudgetData')

    @staticmethod
    def from_obj(args, reset=False, sync=True, **kwargs):
        try:
            kwargs['budgetname'] = args.budgetname
            kwargs['nynabconnection'] = nYnabConnection(args.email, args.password)
            if hasattr(args, 'engine'):
                kwargs['engine'] = args.engine

            client = nYnabClient(**kwargs)
            if sync:
                client.sync()
            if reset:
                # deletes the budget
                client.delete_budget(args.budgetname)
                client.create_budget(args.budgetname)
                client.select_budget(args.budgetname)
            return client
        except BudgetNotFound:
            print('No budget by the name %s found in nYNAB' % args.budgetname)
            exit(-1)

    @property
    def extra_catalog(self):
        return dict(user_id=self.connection.user_id)

    @property
    def extra_budget(self):
        return dict(calculated_entities_included=False, budget_version_id=self.budget_version_id)

    def sync_catalog(self):
        self.catalogClient.sync(extra=self.extra_catalog)

    def sync_budget(self):
        self.budgetClient.sync(extra=self.extra_budget)

    def sync(self):
        if self.connection is None:
            return
        self.logger.debug('Client.sync')

        self.sync_catalog()
        self.select_budget(self.budget_name)
        self.sync_budget()

        if self.budget_version_id is None and self.budget_name is not None:
            raise BudgetNotFound()

    def push_budget(self):
        self.budgetClient.push(extra=self.extra_budget)

    def push_catalog(self):
        self.catalogClient.push(extra=self.extra_catalog)

    def push(self, expected_delta=1):
        if self.connection is None:
            return
        # ending-starting represents the number of modifications that have been done to the data ?
        self.logger.debug('Client.push')

        catalog_changed_entities = self.catalog.get_changed_apidict()
        budget_changed_entities = self.budget.get_changed_apidict()

        delta = sum(len(l) for k, l in catalog_changed_entities.items()) + \
            sum(len(l) for k, l in budget_changed_entities.items())

        if delta != expected_delta:
            raise WrongPushException(expected_delta, delta)

        if any(catalog_changed_entities) or any(budget_changed_entities):
            self.ending_device_knowledge = self.starting_device_knowledge + 1

        self.push_catalog()
        self.push_budget()

        self.starting_device_knowledge = self.ending_device_knowledge
        self.session.commit()

    @operation(3)
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

    @operation(1)
    def delete_account(self, account):
        self.budget.be_accounts.remove(account)

    @operation(1)
    def add_transaction(self, transaction):
        self.budget.be_transactions.append(transaction)

    def add_transactions(self, transaction_list):
        for chunkelement in chunk(transaction_list, 50):
            self._add_transactions(chunkelement)

    @property
    def _add_transactions(self, transaction_list):
        @operation(len(transaction_list))
        def _add_transactions_method(self, transaction_list):
            for transaction in transaction_list:
                self.budget.be_transactions.append(transaction)
        return _add_transactions_method

    @operation(1)
    def delete_transaction(self, transaction):
        self.budget.be_transactions.remove(transaction)

    @operation(1)
    def delete_budget(self, budget_name):
        for budget in self.catalog.ce_budgets:
            if budget.budget_name == budget_name:
                self.catalog.ce_budgets.remove(budget)

    def select_budget(self, budget_name):
        self.budget_version_id = None
        for budget_version in self.catalog.ce_budget_versions:
            if budget_version.version_name == budget_name:
                self.budget_version_id = budget_version.id
        if self.budget_version_id is None:
            raise BudgetNotFound()

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


def clientfromargs(args, reset=False, sync=True):
    return nYnabClient.from_obj(args, reset, sync)