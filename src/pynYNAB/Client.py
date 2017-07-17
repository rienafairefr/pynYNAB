import logging

from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.schema import nYnabClient_

LOG = logging.getLogger(__name__)


class nYnabClient(object):
    def __new__(cls, *args, **kwargs):
        connection = kwargs.pop('nynabconnection', None)

        class Args(object):
            budget_name = kwargs.pop('budgetname', None)
            email = connection.email if hasattr(connection, 'email') else kwargs.pop('email', '')
            password = connection.password if hasattr(connection, 'password') else kwargs.pop('password', '')
            nynabconnection = connection

        passed = Args()
        factory = nYnabClientFactory()
        return factory.create_client(passed)
