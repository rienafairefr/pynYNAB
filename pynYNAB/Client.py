import logging
from functools import wraps

import bcrypt as bcrypt
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from pynYNAB.ObjClient import RootObjClient
from pynYNAB.connection import nYnabConnection
from pynYNAB.exceptions import BudgetNotFound, WrongPushException
from pynYNAB.schema.ClientData import nYnabClientData, Knowledge
from pynYNAB.schema.Entity import Base
from pynYNAB.schema.budget import Payee, Transaction
from pynYNAB.schema.roots import Budget
from pynYNAB.schema.roots import Catalog
from pynYNAB.utils import get_one_or_create

LOG = logging.getLogger(__name__)


def operation(expected_delta):
    def operation_decorator(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            fn(self, *args, **kwargs)
            LOG.debug('push after '+fn.__name__)
            self.push(expected_delta)
        return wrapped
    return operation_decorator


class CatalogClient(RootObjClient):
    @property
    def extra(self):
        return dict(user_id=self.client.connection.user_id)

    opname = 'syncCatalogData'


class BudgetClient(RootObjClient):
    @property
    def extra(self):
        return dict(calculated_entities_included=False, budget_version_id=self.client.budget_version_id)

    opname = 'syncBudgetData'


class NoBudgetNameException(Exception):
    pass

class nYnabClientFactory(object):
    @staticmethod
    def from_obj(args, sync=True, **kwargs):
        try:
            kwargs['budgetname'] = args.budgetname
            if not hasattr(args, 'nynabconnection'):
                nynabconnection = nYnabConnection(args.email, args.password)
            else:
                nynabconnection = args.nynabconnection
            if hasattr(args, 'engine'):
                kwargs['engine'] = args.engine

            client_id = get_id(args.email,args.password)

            engine = create_engine(kwargs.get('engine', 'sqlite://'))

            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            session = Session()

            client_data,created = get_one_or_create(session,nYnabClientData,
                                                    id=client_id,
                                                    budget_name = args.budgetname)
            if created:
                client_data.catalog = Catalog()
                client_data.catalog.knowledge = Knowledge()
                client_data.budget = Budget()
                client_data.budget.knowledge = Knowledge()

                session.add(client_data.catalog)
                session.add(client_data.budget)

            client = nYnabClient(client_data, nynabconnection, session)
            if sync:
                client.sync()
            return client
        except BudgetNotFound:
            print('No budget by the name %s found in nYNAB' % args.budgetname)
            exit(-1)

def get_id(email,password):
    return bcrypt.hashpw(email+password,bcrypt.gensalt())


class nYnabClient(object):
    def __init__(self, data, connection, session):
        self.budget_version_id = data.budget_version_id
        self.budget_name = data.budget_name
        self.connection = connection
        self.session = session
        self.catalogClient = CatalogClient(data.catalog, self)
        self.catalog = data.catalog
        self.budgetClient = BudgetClient(data.budget, self)
        self.budget = data.budget
        self.server_entities=None
        self.starting_device_knowledge = data.starting_device_knowledge
        self.ending_device_knowledge = data.ending_device_knowledge

        if self.budget_name is None:
            LOG.error('No budget name was provided')
            raise NoBudgetNameException
        if self.connection is not None:
            self.connection.init_session()

    def sync(self):
        LOG.debug('Client.sync')

        self.catalogClient.sync()
        self.select_budget(self.budget_name)
        self.budgetClient.sync()

        if self.budget_version_id is None and self.budget_name is not None:
            raise BudgetNotFound()

    def push(self, expected_delta=1):
        # ending-starting represents the number of modifications that have been done to the data ?
        LOG.debug('Client.push')

        catalog_changed_entities = self.catalog.get_changed_apidict()
        budget_changed_entities = self.budget.get_changed_apidict()

        delta = sum(len(l) for k, l in catalog_changed_entities.items()) + \
            sum(len(l) for k, l in budget_changed_entities.items())

        if delta != expected_delta:
            raise WrongPushException(expected_delta, delta)

        if any(catalog_changed_entities) or any(budget_changed_entities):
            self.ending_device_knowledge = self.starting_device_knowledge + 1

        self.catalogClient.push()
        self.budgetClient.push()

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
        pass

    @operation(1)
    def delete_account(self, account):
        self.budget.be_accounts.remove(account)

    @operation(1)
    def add_transaction(self, transaction):
        self.budget.be_transactions.append(transaction)

    def add_transactions(self, transaction_list):
        @operation(len(transaction_list))
        def _add_transactions_method(self, tr_list):
            for tr in tr_list:
                self.budget.be_transactions.append(tr)

        return _add_transactions_method(transaction_list)

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


def clientfromargs(args, sync=True):
    return nYnabClientFactory.from_obj(args, sync)