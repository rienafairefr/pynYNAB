import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.ObjClient import RootObjClient
from pynYNAB.connection import nYnabConnection
from pynYNAB.exceptions import NoBudgetNameException, BudgetNotFound, NoCredentialsException
from pynYNAB.schema import Base, Catalog, Budget

LOG = logging.getLogger(__name__)


class CatalogClient(RootObjClient):
    @property
    def extra(self):
        return dict(user_id=self.client.user_id)

    opname = 'syncCatalogData'
    prefix = 'ce_'

    def __init__(self, client):
        super(CatalogClient, self).__init__(client.catalog, client, Catalog)


class BudgetClient(RootObjClient):
    @property
    def extra(self):
        return dict(calculated_entities_included=False, budget_version_id=self.client.budget_version_id)

    opname = 'syncBudgetData'
    prefix = 'be_'

    def __init__(self, client):
        super(BudgetClient, self).__init__(client.budget, client, Budget)

    def get_changed_apidict(self):
        changed_api_dict = super(BudgetClient, self).get_changed_apidict()
        if 'transactions' in changed_api_dict:
            changed_api_dict['transaction_groups'] = []
            for transaction_dict in changed_api_dict.pop('transactions'):
                transaction_id = transaction_dict['id']
                subtransactions = []
                if 'subtransactions' in changed_api_dict:
                    for subtransaction_dic in changed_api_dict['subtransactions']:
                        if subtransaction_dic['entities_transaction_id'] == transaction_id:
                            subtransactions.append(subtransaction_dic)
                    for subtransaction in subtransactions:
                        changed_api_dict['subtransactions'].remove(subtransaction)
                if not subtransactions:
                    subtransactions = None
                group = dict(
                    id=transaction_id,
                    transaction=transaction_dict,
                    subtransactions=subtransactions,
                    matched_transaction=None)
                changed_api_dict['transaction_groups'].append(group)
        if changed_api_dict.get('subtransactions') is not None:
            del changed_api_dict['subtransactions']
        return changed_api_dict


class nYnabClientFactory(object):
    def __init__(self, engine_url='sqlite:///:memory:', engine=None):
        self.engine_url = engine_url
        if engine is None:
            self.engine = create_engine(engine_url)
        else:
            self.engine = engine

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_client(self, email=None, password=None, budget_name=None, connection=None, sync=True):
        from pynYNAB.schema.Client import nYnabClient_

        if budget_name is None:
            raise NoBudgetNameException

        try:
            if connection is None:
                if email is None and password is None:
                    raise NoCredentialsException()
                connection = nYnabConnection(email, password)
                connection.init_session()

            client_id = connection.id

            def postprocessed_client(cl):
                cl.connection = connection
                cl.catalogClient = CatalogClient(cl)
                cl.budgetClient = BudgetClient(cl)
                return cl

            previous_client = self.session.query(nYnabClient_).get(client_id)
            if previous_client is not None:
                previous_client.session = self.session
                return postprocessed_client(previous_client)

            client = nYnabClient_(id=client_id, budget_name=budget_name)
            client.engine = self.engine
            client.session = self.session
            client.add_missing()
            client = postprocessed_client(client)

            self.session.add(client)
            client.session.commit()
            if sync:
                client.sync()
            return client
        except BudgetNotFound:
            LOG.error('No budget by the name %s found in nYNAB' % budget_name)
            raise

    @classmethod
    def from_args(cls, args, sync=True):
        return nYnabClientFactory().create_client(args.email, args.password, args.budget_name, args.connection, sync)

    @classmethod
    def from_kwargs(cls, **kwargs):
        return nYnabClientFactory().create_client(kwargs.get("email", None),
                                                  kwargs.get("password", None),
                                                  kwargs.get("budget_name", None),
                                                  kwargs.get("connection", None),
                                                  kwargs.get("sync", True))


def clientfromargs(args, sync=True):
    return nYnabClientFactory.from_args(args, sync)


def clientfromkwargs(**kwargs):
    return nYnabClientFactory.from_kwargs(**kwargs)
