# ynab_api.TransactionsApi

All URIs are relative to *https://api.youneedabudget.com/papi/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk_create_transactions**](TransactionsApi.md#bulk_create_transactions) | **POST** /budgets/{budget_id}/transactions/bulk | Bulk create transactions
[**create_transaction**](TransactionsApi.md#create_transaction) | **POST** /budgets/{budget_id}/transactions | Create new transaction
[**get_transactions**](TransactionsApi.md#get_transactions) | **GET** /budgets/{budget_id}/transactions | List transactions
[**get_transactions_by_account**](TransactionsApi.md#get_transactions_by_account) | **GET** /budgets/{budget_id}/accounts/{account_id}/transactions | List account transactions
[**get_transactions_by_category**](TransactionsApi.md#get_transactions_by_category) | **GET** /budgets/{budget_id}/categories/{category_id}/transactions | List category transactions
[**get_transactions_by_id**](TransactionsApi.md#get_transactions_by_id) | **GET** /budgets/{budget_id}/transactions/{transaction_id} | Single transaction
[**update_transaction**](TransactionsApi.md#update_transaction) | **PUT** /budgets/{budget_id}/transactions/{transaction_id} | Updates an existing transaction


# **bulk_create_transactions**
> BulkTransactionCreateResponse bulk_create_transactions(budget_id, transactions)

Bulk create transactions

Creates multiple transactions

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
transactions = ynab_api.BulkTransactions() # BulkTransactions | The list of Transactions to create.

try:
    # Bulk create transactions
    api_response = api_instance.bulk_create_transactions(budget_id, transactions)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->bulk_create_transactions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **transactions** | [**BulkTransactions**](BulkTransactions.md)| The list of Transactions to create. | 

### Return type

[**BulkTransactionCreateResponse**](BulkTransactionCreateResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_transaction**
> TransactionResponse create_transaction(budget_id, transaction)

Create new transaction

Creates a transaction

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
transaction = ynab_api.SaveTransactionWrapper() # SaveTransactionWrapper | The Transaction to create.

try:
    # Create new transaction
    api_response = api_instance.create_transaction(budget_id, transaction)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->create_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **transaction** | [**SaveTransactionWrapper**](SaveTransactionWrapper.md)| The Transaction to create. | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transactions**
> TransactionsResponse get_transactions(budget_id, since_date=since_date, type=type)

List transactions

Returns budget transactions

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
since_date = '2013-10-20' # date | Only return transactions on or after this date. (optional)
type = 'type_example' # str | Only return transactions of a certain type (i.e. 'uncategorized', 'unapproved') (optional)

try:
    # List transactions
    api_response = api_instance.get_transactions(budget_id, since_date=since_date, type=type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->get_transactions: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **since_date** | **date**| Only return transactions on or after this date. | [optional] 
 **type** | **str**| Only return transactions of a certain type (i.e. &#39;uncategorized&#39;, &#39;unapproved&#39;) | [optional] 

### Return type

[**TransactionsResponse**](TransactionsResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transactions_by_account**
> TransactionsResponse get_transactions_by_account(budget_id, account_id, since_date=since_date)

List account transactions

Returns all transactions for a specified account

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
account_id = 'account_id_example' # str | The ID of the Account.
since_date = '2013-10-20' # date | Only return transactions on or after this date. (optional)

try:
    # List account transactions
    api_response = api_instance.get_transactions_by_account(budget_id, account_id, since_date=since_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->get_transactions_by_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **account_id** | [**str**](.md)| The ID of the Account. | 
 **since_date** | **date**| Only return transactions on or after this date. | [optional] 

### Return type

[**TransactionsResponse**](TransactionsResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transactions_by_category**
> TransactionsResponse get_transactions_by_category(budget_id, category_id, since_date=since_date)

List category transactions

Returns all transactions for a specified category

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
category_id = 'category_id_example' # str | The ID of the Category.
since_date = '2013-10-20' # date | Only return transactions on or after this date. (optional)

try:
    # List category transactions
    api_response = api_instance.get_transactions_by_category(budget_id, category_id, since_date=since_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->get_transactions_by_category: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **category_id** | [**str**](.md)| The ID of the Category. | 
 **since_date** | **date**| Only return transactions on or after this date. | [optional] 

### Return type

[**TransactionsResponse**](TransactionsResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_transactions_by_id**
> TransactionResponse get_transactions_by_id(budget_id, transaction_id)

Single transaction

Returns a single transaction

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
transaction_id = 'transaction_id_example' # str | The ID of the Transaction.

try:
    # Single transaction
    api_response = api_instance.get_transactions_by_id(budget_id, transaction_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->get_transactions_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **transaction_id** | [**str**](.md)| The ID of the Transaction. | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_transaction**
> TransactionResponse update_transaction(budget_id, transaction_id, transaction)

Updates an existing transaction

Updates a transaction

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
api_instance = ynab_api.TransactionsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
transaction_id = 'transaction_id_example' # str | The ID of the Transaction.
transaction = ynab_api.SaveTransactionWrapper() # SaveTransactionWrapper | The Transaction to update.

try:
    # Updates an existing transaction
    api_response = api_instance.update_transaction(budget_id, transaction_id, transaction)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->update_transaction: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **transaction_id** | [**str**](.md)| The ID of the Transaction. | 
 **transaction** | [**SaveTransactionWrapper**](SaveTransactionWrapper.md)| The Transaction to update. | 

### Return type

[**TransactionResponse**](TransactionResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

