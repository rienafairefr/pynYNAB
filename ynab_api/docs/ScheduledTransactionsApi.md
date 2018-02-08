# ynab_api.ScheduledTransactionsApi

All URIs are relative to *https://api.youneedabudget.com/papi/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_scheduled_transaction_by_id**](ScheduledTransactionsApi.md#get_scheduled_transaction_by_id) | **GET** /budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id} | Single scheduled transaction
[**get_scheduled_transactions**](ScheduledTransactionsApi.md#get_scheduled_transactions) | **GET** /budgets/{budget_id}/scheduled_transactions | List scheduled transactions


# **get_scheduled_transaction_by_id**
> ScheduledTransactionResponse get_scheduled_transaction_by_id(budget_id, scheduled_transaction_id)

Single scheduled transaction

Returns a single scheduled transaction

### Example
```python
from __future__ import print_function
import time
import ynab_api
from ynab_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: bearer
configuration = ynab_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = ynab_api.ScheduledTransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
scheduled_transaction_id = 'scheduled_transaction_id_example' # str | The ID of the Scheduled Transaction.

try:
    # Single scheduled transaction
    api_response = api_instance.get_scheduled_transaction_by_id(budget_id, scheduled_transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScheduledTransactionsApi->get_scheduled_transaction_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **scheduled_transaction_id** | [**str**](.md)| The ID of the Scheduled Transaction. | 

### Return type

[**ScheduledTransactionResponse**](ScheduledTransactionResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_scheduled_transactions**
> ScheduledTransactionsResponse get_scheduled_transactions(budget_id)

List scheduled transactions

Returns all scheduled transactions

### Example
```python
from __future__ import print_function
import time
import ynab_api
from ynab_api.rest import ApiException
from pprint import pprint

# Configure API key authorization: bearer
configuration = ynab_api.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = ynab_api.ScheduledTransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.

try:
    # List scheduled transactions
    api_response = api_instance.get_scheduled_transactions(budget_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ScheduledTransactionsApi->get_scheduled_transactions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 

### Return type

[**ScheduledTransactionsResponse**](ScheduledTransactionsResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

