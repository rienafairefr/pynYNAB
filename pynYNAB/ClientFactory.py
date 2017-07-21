import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pynYNAB.ObjClient import RootObjClient
from pynYNAB.connection import nYnabConnection
from pynYNAB.exceptions import NoBudgetNameException, BudgetNotFound, NoCredentialsException
from pynYNAB.schema import Base


LOG = logging.getLogger(__name__)


class CatalogClient(RootObjClient):
    @property
    def extra(self):
        return dict(user_id=self.client.user_id)

    opname = 'syncCatalogData'

    def __init__(self, client):
        super(CatalogClient, self).__init__(client.catalog, client)


class BudgetClient(RootObjClient):
    @property
    def extra(self):
        return dict(calculated_entities_included=False, budget_version_id=self.client.budget_version_id)

    opname = 'syncBudgetData'

    def __init__(self, client):
        super(BudgetClient, self).__init__(client.budget, client)


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

    def create_client(self, args=None, sync=True, **kwargs):
        from pynYNAB.schema.Client import nYnabClient_
        if args is None:
            class Arg(object):pass
            args = Arg()
        for k,v in kwargs.items():
            setattr(args,k,v)
        if hasattr(args,'budgetname'):
            setattr(args, 'budget_name', args.budgetname)

        if hasattr(args, 'nynabconnection') and args.nynabconnection is not None:
            setattr(args, 'connection', args.nynabconnection)

        if not hasattr(args, 'budget_name') or args.budget_name is None:
            raise NoBudgetNameException

        try:
            if not hasattr(args, 'connection'):
                if not hasattr(args, 'email') or args.email is None:
                    if not hasattr(args, 'password') or args.password is None:
                        raise NoCredentialsException
                connection = nYnabConnection(args.email, args.password)
                connection.init_session()
            else:
                connection = args.connection

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

            client = nYnabClient_(id=client_id, budget_name=args.budget_name)
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
            LOG.error('No budget by the name %s found in nYNAB' % args.budget_name)
            raise


def clientfromargs(args, sync=True):
    return nYnabClientFactory().create_client(args, sync)