from __future__ import print_function
import time

import os

import ynab_api
from pprint import pprint
from dotenv import load_dotenv,find_dotenv

from ynab_api.rest import ApiException

load_dotenv(find_dotenv())

# Configure API key authorization: bearer
ynab_api.configuration.api_key['Authorization'] = os.environ.get('YNAB_API_TOKEN')
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# ynab_api.configuration.api_key_prefix['Authorization'] = 'Bearer'
# create an instance of the API class
api_instance = ynab_api.AccountsApi()
budget_id = 'budget_id_example' # str | The ID of the Budget.
account_id = 'account_id_example' # str | The ID of the Account.

try:
    # Single account
    api_response = api_instance.get_account_by_id(budget_id, account_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AccountsApi->get_account_by_id: %s\n" % e)