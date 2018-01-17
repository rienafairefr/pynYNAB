import logging
import os

import datetime
from pynYNAB.ClientFactory import nYnabClientFactory
from sqlalchemy import create_engine
import json
import settings


class MockConnection(object):
    user_id = '1'
    id = '1c1ba2d2-b31e-4b67-a76d-03c47cbf826b'
    directory = None

    def __init__(self, directory=None):
        if directory is not None:
            self.directory = directory

    def init_session(self):
        pass

    def dorequest(self, request_dic, opname):
        p = '{}/{}.json'.format(self.directory, opname)
        if not os.path.exists(p):
            return None
        with open(p, 'r') as f:
            data = json.load(f)
            return data


class nYnabOfflineClient(object):
    def __new__(cls, *args, **kwargs):
        connection = kwargs.pop('nynabconnection', None)

        class Args(object):
            budget_name = kwargs.pop('budgetname', None)
            email = connection.email if hasattr(connection, 'email') else kwargs.pop('email', '')
            password = connection.password if hasattr(connection, 'password') else kwargs.pop('password', '')
            nynabconnection = connection
            db_path = 'offline'

        passed = Args()
        if hasattr(passed, 'db_path'):
            logging.info('Creating client from server...')
            factory = nYnabClientFactory(
                engine=create_engine('sqlite:///{}/{}.db'.format(passed.db_path, settings.ynab_budget)))
        else:
            logging.info('Creating client from database...')
            factory = nYnabClientFactory(engine=create_engine('sqlite:///:memory:'))
        return factory.create_client(passed, sync=False)


class OfflineBudget:
    directory = 'offline'

    def __init__(self, action='load'):
        # create directory where to store the offline budget
        self.client = None
        try:
            os.mkdir(self.directory)
        except OSError as e:
            if e.errno == 17:
                pass
            else:
                raise e

        if action == 'load':
            self.client = self.load_offline_client()
        else:
            self.sync_offline_client()

    def write_file(self, client, entity):
        a = getattr(client, entity)
        with open('{}/{}-{}.json'.format(self.directory, entity, settings.ynab_budget), 'w') as f:
            data = a.get_dict()
            logging.info('Writing {}: {}'.format(entity, data))
            json.dump(data, f)

    def read_file(self, entity):
        with open('{}/{}-{}.json'.format(self.directory, entity, settings.ynab_budget), 'r') as f:
            data = json.load(f)
            logging.info('Found {}: {}'.format(entity, data))
            return data

    def sync_offline_client(self):
        client = nYnabOfflineClient(email=settings.ynab_username, password=settings.ynab_password,
                                    budgetname=settings.ynab_budget,
                                    logger=settings.log, db_path=self.directory)
        if os.path.exists('{}/db-{}.db'.format(self.directory, settings.ynab_budget)):
            try:
                self.read_file('budget')
                self.read_file('catalog')
                logging.warn('Old offline budget found. Skipping...')
                return
            except (ValueError, IOError) as e:
                logging.info('Error parsing offline files: {}'.format(e.message))

        client.sync()
        self.write_file(client, 'budget')
        self.write_file(client, 'catalog')

    def load_offline_client(self):
        try:
            self.client = self._load()
        except (IOError, AttributeError, ValueError) as e:
            self.sync_offline_client()
            self.client = self._load()

        logging.debug('Loaded offline client')
        return self.client

    def _load(self):
        client = nYnabOfflineClient(email=settings.ynab_username, password=settings.ynab_password,
                                    budgetname=settings.ynab_budget,
                                    logger=settings.log, nynabconnection=MockConnection(directory=self.directory))
        client.budget.from_dict(self.read_file('budget'))
        client.catalog.from_dict(self.read_file('catalog'))
        return client


if __name__ == '__main__':
    OfflineBudget(action='load')

