from __future__ import print_function

import os
import unittest

from dotenv import load_dotenv, find_dotenv
from ynab_api import BudgetsApi

from ynab_api.configuration import Configuration
from ynab_api.rest import ApiException
from ynab_api.api_client import ApiClient

load_dotenv(find_dotenv())

configuration = Configuration()
configuration.api_key['Authorization'] = 'Bearer ' + os.environ.get('YNAB_API_TOKEN')
api_client = ApiClient(configuration)

api_instance = BudgetsApi(api_client)


class TestNewApiBudget(unittest.TestCase):
    def test_find_test_budget(self):
        searched = 'Test Budget - Dont Remove'

        budgets = api_instance.get_budgets().data.budgets
        for budget in budgets:
            if budget.name == searched:
                return
        print('Couldnt find the "%s" budget' % searched)
        exit(-1)
