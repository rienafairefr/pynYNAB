# ynab.CategoriesApi

All URIs are relative to *https://api.youneedabudget.com/papi/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_categories**](CategoriesApi.md#get_categories) | **GET** /budgets/{budget_id}/categories | List categories
[**get_category_by_id**](CategoriesApi.md#get_category_by_id) | **GET** /budgets/{budget_id}/categories/{category_id} | Single category


# **get_categories**
> CategoriesResponse get_categories(budget_id)

List categories

Returns all categories grouped by category group.

### Example
```python
from __future__ import print_function
import time
import ynab
from ynab.rest import ApiException
from pprint import pprint

# Configure API key authorization: bearer
configuration = ynab.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = ynab.CategoriesApi(ynab.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.

try:
    # List categories
    api_response = api_instance.get_categories(budget_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CategoriesApi->get_categories: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 

### Return type

[**CategoriesResponse**](CategoriesResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_category_by_id**
> CategoryResponse get_category_by_id(budget_id, category_id)

Single category

Returns a single category

### Example
```python
from __future__ import print_function
import time
import ynab
from ynab.rest import ApiException
from pprint import pprint

# Configure API key authorization: bearer
configuration = ynab.Configuration()
configuration.api_key['Authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
api_instance = ynab.CategoriesApi(ynab.ApiClient(configuration))
budget_id = 'budget_id_example' # str | The ID of the Budget.
category_id = 'category_id_example' # str | The ID of the Category.

try:
    # Single category
    api_response = api_instance.get_category_by_id(budget_id, category_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CategoriesApi->get_category_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **budget_id** | [**str**](.md)| The ID of the Budget. | 
 **category_id** | [**str**](.md)| The ID of the Category. | 

### Return type

[**CategoryResponse**](CategoryResponse.md)

### Authorization

[bearer](../README.md#bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

