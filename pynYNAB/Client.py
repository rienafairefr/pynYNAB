import logging

from pynYNAB.ClientFactory import nYnabClientFactory

LOG = logging.getLogger(__name__)


class nYnabClient(object):
    def __new__(cls, *args, **kwargs):
        connection = kwargs.pop('nynabconnection', None)
        email = connection.email if hasattr(connection, 'email') else kwargs.pop('email', '')
        password = connection.password if hasattr(connection, 'password') else kwargs.pop('password', '')
        budget_name = kwargs.pop('budgetname', None)
        
        factory = nYnabClientFactory()
        return factory.create_client(email, password, budget_name, connection)
