# ynab_api.PayeesApi

All URIs are relative to *https://api.youneedabudget.com/papi/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_payee_by_id**](PayeesApi.md#get_payee_by_id) | **GET** /budgets/{budget_id}/payees/{payee_id} | Single payee
[**get_payees**](PayeesApi.md#get_payees) | **GET** /budgets/{budget_id}/payees | List payees


# **get_payee_by_id**
> PayeeResponse get_payee_by_id(budget_id, payee_id)

Single payee

Returns single payee

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
api_instance = ynab_api.PayeesApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
payee_id = 'payee_id_example' # str | The ID of the Payee.

try:
    # Single payee
    api_response = api_instance.get_payee_by_id(budget_id, payee_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayeesApi->get_payee_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **payee_id** | [**str**](.md)| The ID of the Payee. | 

### Return type

[**PayeeResponse**](PayeeResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_payees**
> PayeesResponse get_payees(budget_id)

List payees

Returns all payees

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
api_instance = ynab_api.PayeesApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.

try:
    # List payees
    api_response = api_instance.get_payees(budget_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PayeesApi->get_payees: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 

### Return type

[**PayeesResponse**](PayeesResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

