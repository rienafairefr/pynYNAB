# ynab_api.BudgetsApi

All URIs are relative to *https://api.youneedabudget.com/papi/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_budget_by_id**](BudgetsApi.md#get_budget_by_id) | **GET** /budgets/{budget_id} | Single budget
[**get_budgets**](BudgetsApi.md#get_budgets) | **GET** /budgets | List budgets


# **get_budget_by_id**
> BudgetDetailResponse get_budget_by_id(budget_id, last_knowledge_of_server=last_knowledge_of_server)

Single budget

Returns a single budget with all related entities.  This resource is effectively a full budget export.

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
api_instance = ynab_api.BudgetsApi(ynab_api.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
last_knowledge_of_server = 8.14 # float | The starting server knowledge.  If provided, only entities that have changed since last_knowledge_of_server will be included. (optional)

try:
    # Single budget
    api_response = api_instance.get_budget_by_id(budget_id, last_knowledge_of_server=last_knowledge_of_server)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BudgetsApi->get_budget_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **last_knowledge_of_server** | **float**| The starting server knowledge.  If provided, only entities that have changed since last_knowledge_of_server will be included. | [optional] 

### Return type

[**BudgetDetailResponse**](BudgetDetailResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_budgets**
> BudgetSummaryResponse get_budgets()

List budgets

Returns budgets list with summary information.

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
api_instance = ynab_api.BudgetsApi(ynab_api.ApiClient(configuration))

try:
    # List budgets
    api_response = api_instance.get_budgets()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BudgetsApi->get_budgets: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BudgetSummaryResponse**](BudgetSummaryResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

