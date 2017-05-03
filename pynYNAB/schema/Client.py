import logging
from functools import wraps

from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from pynYNAB.exceptions import BudgetNotFound, WrongPushException
from pynYNAB.schema import Base, Catalog, Budget, Knowledge, Payee, Transaction

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


class nYnabClient_(Base):
    __tablename__ = "nynabclients"
    id = Column(String, primary_key=True)
    catalog_id = Column(ForeignKey('catalog.id'))
    catalog = relationship('Catalog')
    budget_id = Column(ForeignKey('budget.id'))
    budget = relationship('Budget')
    budget_version_id = Column(String)
    budget_name = Column(String)
    starting_device_knowledge = Column(Integer, default=0)
    ending_device_knowledge = Column(Integer, default=0)
    connection = None
    session = None

    @property
    def user_id(self):
        return self.id

    @property
    def online(self):
        return self.connection is not None

    def add_missing(self):
        self.catalog = Catalog()
        self.catalog.knowledge = Knowledge()
        self.budget = Budget()
        self.budget.knowledge = Knowledge()
        self.session.add(self.catalog)
        self.session.add(self.budget)
        self.session.commit()

    def init_internal_db(self):
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def sync(self, update_keys=None):
        LOG.debug('Client.sync')

        self.catalogClient.sync(update_keys)
        self.select_budget(self.budget_name)
        self.budgetClient.sync(update_keys)

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

