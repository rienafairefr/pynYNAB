from __future__ import print_function
import time

import os

from pprint import pprint
from dotenv import load_dotenv,find_dotenv

from pynYNAB.ynab_api.api.accounts_api import AccountsApi
from pynYNAB.ynab_api.configuration import Configuration
from pynYNAB.ynab_api.rest import ApiException
from pynYNAB.ynab_api.api_client import ApiClient

load_dotenv(find_dotenv())

# Configure API key authorization: bearer
configuration = Configuration()

configuration.api_key['Authorization'] = os.environ.get('YNAB_API_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
api_client = ApiClient(configuration)
# create an instance of the API class
api_instance = AccountsApi(api_client)
budget_id = 'budget_id_example' # str | The ID of the Budget.
account_id = 'account_id_example' # str | The ID of the Account.

try:
    # Single account
    api_response = api_instance.get_account_by_id(budget_id, account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountsApi->get_account_by_id: %s\n" % e)