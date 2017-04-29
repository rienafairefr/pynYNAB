from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from pynYNAB.connection import nYnabConnection
from pynYNAB.exceptions import NoBudgetNameException, BudgetNotFound
from pynYNAB.schema import Base


class nYnabClientFactory(object):
    def __init__(self, engine_url='sqlite://'):
        self.engine_url = engine_url
        self.engine = create_engine(engine_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_client(self, args=None, sync=True, **kwargs):
        from pynYNAB.Client import get_id, nYnabClient_, CatalogClient, BudgetClient
        if args is not None:
            args.__dict__.update(kwargs)
        if hasattr(args,'budgetname'):
            setattr(args, 'budget_name', args.budgetname)

        if not hasattr(args, 'budget_name') or args.budget_name is None:
            raise NoBudgetNameException

        try:
            if not hasattr(args, 'nynabconnection'):
                connection = nYnabConnection(args.email, args.password)
            else:
                connection = args.nynabconnection

            client_id = connection.user_id

            previous_client = self.session.query(nYnabClient_).get(client_id)
            if previous_client is not None:
                previous_client.catalogClient = CatalogClient(previous_client)
                previous_client.budgetClient = BudgetClient(previous_client)
                return previous_client

            client = nYnabClient_(id=client_id, budget_name=args.budgetname)
            client.engine = self.engine

            client.init_internal_db()
            client.add_missing()
            client.session.add(client)
            client.session.commit()
            if sync:
                client.sync()
            return client
        except BudgetNotFound:
            print('No budget by the name %s found in nYNAB' % args.budgetname)
            exit(-1)


def clientfromargs(args, sync=True):
    return nYnabClientFactory().create_client(args, sync)