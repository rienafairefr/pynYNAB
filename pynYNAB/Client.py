import logging
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.Entity import Base
from pynYNAB.schema.budget import Payee, Transaction
from pynYNAB.schema.catalog import BudgetVersion
from pynYNAB.schema.roots import Budget
from pynYNAB.schema.roots import Catalog
from pynYNAB.scripts.config import get_logger
from pynYNAB.utils import chunk

logger = logging.getLogger('pynYNAB')


def clientfromargs(args, reset=False):
    return nYnabClient.from_obj(args, reset)


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
            self.push(expected_delta)
        return wrapped
    return operation_decorator


class nYnabClient(object):
    def __init__(self, **kwargs):
        self.server_entities = {}
        self.budget_version_id = None
        self.logger = kwargs.get('logger', None)
        if self.logger is None:
            self.logger = get_logger()

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

        self.first = True
        self.online = self.connection is not None
        if self.connection is not None:
            self.sync()

    @staticmethod
    def from_obj(args, reset=False, **kwargs):
        try:
            if not hasattr(args, 'logginglevel'):
                setattr(args, 'logginglevel', 'error')

            kwargs['logger'] = get_logger(args)
            kwargs['budgetname'] = args.budgetname
            kwargs['nynabconnection'] = nYnabConnection(args.email, args.password)
            if hasattr(args, 'engine'):
                kwargs['engine'] = args.engine

            client = nYnabClient(**kwargs)
            if reset:
                # deletes the budget
                client.delete_budget(args.budgetname)
                client.create_budget(args.budgetname)
                client.select_budget(args.budgetname)
            return client
        except BudgetNotFound:
            print('No budget by the name %s found in nYNAB' % args.budgetname)
            exit(-1)

    def sync(self):
        if self.connection is None:
            return
        self.logger.debug('Client.sync')

        self.sync_obj(self.catalog, 'syncCatalogData', extra=dict(user_id=self.connection.user_id))
        self.select_budget(self.budget_name)

        self.sync_obj(self.budget, 'syncBudgetData',
                      extra=dict(
                          calculated_entities_included=False,
                          budget_version_id=self.budget_version_id)
                      )
        if self.budget_version_id is None and self.budget_name is not None:
            raise BudgetNotFound()

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
        self._push_obj(self.catalog, 'syncCatalogData', extra=dict(user_id=self.connection.user_id))
        self._push_obj(self.budget, 'syncBudgetData',
                       extra=dict(
                          calculated_entities_included=False,
                          budget_version_id=self.budget_version_id))
        self.starting_device_knowledge = self.ending_device_knowledge
        self.session.commit()

    def update_from_api_changed_entities(self, obj, changed_entities):
        for name in obj.listfields:
            if changed_entities[name] is None:
                continue
            newlist = []
            for entitydict in changed_entities[name]:
                newlist.append(obj.listfields[name].from_apidict(entitydict))
            changed_entities[name] = newlist
        self.update_from_changed_entities(obj, changed_entities)

    def update_from_changed_entities(self, obj, changed_entities):
        for name, value in changed_entities.items():
            if not isinstance(value, list):
                continue
            list_of_entities = getattr(obj, name)
            for incoming_obj in value:
                current_obj = self.session.query(obj.listfields[name]).get(incoming_obj.id)
                if current_obj is not None:
                    if incoming_obj.is_tombstone:
                        self.session.delete(current_obj)
                    else:
                        if current_obj not in list_of_entities:
                            current_obj.parent = obj
                        else:
                            for field in current_obj.scalarfields:
                                incoming = getattr(incoming_obj, field)
                                present = getattr(current_obj, field)
                                if present != incoming:
                                    setattr(current_obj, field, incoming)
                                    pass
                            pass
                else:
                    if not incoming_obj.is_tombstone:
                        self.session.add(incoming_obj)
                        incoming_obj.parent = obj
        self.session.commit()
        pass

    def update_from_sync_data(self, obj, sync_data):
        self.update_from_api_changed_entities(obj, sync_data['changed_entities'])

    def _push_obj(self, obj, opname, extra=None):
        if self.connection is None:
            return
        if extra is None:
            extra = {}

        changed_entities = obj.get_changed_apidict()
        request_data = dict(starting_device_knowledge=self.starting_device_knowledge,
                            ending_device_knowledge=self.ending_device_knowledge,
                            device_knowledge_of_server=self.device_knowledge_of_server[opname],
                            changed_entities=changed_entities)
        request_data.update(extra)
        sync_data = self.connection.dorequest(request_data, opname)
        self.logger.debug('server_knowledge_of_device ' + str(sync_data['server_knowledge_of_device']))
        self.logger.debug('current_server_knowledge ' + str(sync_data['current_server_knowledge']))
        self.update_from_sync_data(obj, sync_data)
        self.session.commit()
        obj.clear_changed_entities()

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

    def sync_obj(self, obj, opname, extra=None):
        if self.connection is None:
            return
        if extra is None:
            extra = {}
        if opname not in self.current_device_knowledge:
            self.current_device_knowledge[opname] = 0
        if opname not in self.device_knowledge_of_server:
            self.device_knowledge_of_server[opname] = 0
            # sync with disregard for knowledge, start from 0
        request_data = dict(starting_device_knowledge=self.starting_device_knowledge,
                            ending_device_knowledge=self.ending_device_knowledge,
                            device_knowledge_of_server=self.device_knowledge_of_server[opname],
                            changed_entities={})

        request_data.update(extra)

        sync_data = self.connection.dorequest(request_data, opname)
        self.server_entities[opname] = sync_data['changed_entities']
        self.logger.debug('server_knowledge_of_device ' + str(sync_data['server_knowledge_of_device']))
        self.logger.debug('current_server_knowledge ' + str(sync_data['current_server_knowledge']))
        self.update_from_sync_data(obj, sync_data)
        self.session.commit()
        obj.clear_changed_entities()

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
