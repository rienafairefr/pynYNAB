# coding: utf-8

"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from pynYnAB.ynab_api.api_client import ApiClient


class TransactionsApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def bulk_create_transactions(self, budget_id, transactions, **kwargs):  # noqa: E501
        """Bulk create transactions  # noqa: E501

        Creates multiple transactions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.bulk_create_transactions(budget_id, transactions, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param BulkTransactions transactions: The list of Transactions to create. (required)
        :return: BulkTransactionCreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.bulk_create_transactions_with_http_info(budget_id, transactions, **kwargs)  # noqa: E501
        else:
            (data) = self.bulk_create_transactions_with_http_info(budget_id, transactions, **kwargs)  # noqa: E501
            return data

    def bulk_create_transactions_with_http_info(self, budget_id, transactions, **kwargs):  # noqa: E501
        """Bulk create transactions  # noqa: E501

        Creates multiple transactions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.bulk_create_transactions_with_http_info(budget_id, transactions, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param BulkTransactions transactions: The list of Transactions to create. (required)
        :return: BulkTransactionCreateResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'transactions']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method bulk_create_transactions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `bulk_create_transactions`")  # noqa: E501
        # verify the required parameter 'transactions' is set
        if ('transactions' not in params or
                params['transactions'] is None):
            raise ValueError("Missing the required parameter `transactions` when calling `bulk_create_transactions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'transactions' in params:
            body_params = params['transactions']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/transactions/bulk', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='BulkTransactionCreateResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def create_transaction(self, budget_id, transaction, **kwargs):  # noqa: E501
        """Create new transaction  # noqa: E501

        Creates a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.create_transaction(budget_id, transaction, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param SaveTransactionWrapper transaction: The Transaction to create. (required)
        :return: TransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.create_transaction_with_http_info(budget_id, transaction, **kwargs)  # noqa: E501
        else:
            (data) = self.create_transaction_with_http_info(budget_id, transaction, **kwargs)  # noqa: E501
            return data

    def create_transaction_with_http_info(self, budget_id, transaction, **kwargs):  # noqa: E501
        """Create new transaction  # noqa: E501

        Creates a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.create_transaction_with_http_info(budget_id, transaction, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param SaveTransactionWrapper transaction: The Transaction to create. (required)
        :return: TransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'transaction']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `create_transaction`")  # noqa: E501
        # verify the required parameter 'transaction' is set
        if ('transaction' not in params or
                params['transaction'] is None):
            raise ValueError("Missing the required parameter `transaction` when calling `create_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'transaction' in params:
            body_params = params['transaction']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/transactions', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transactions(self, budget_id, **kwargs):  # noqa: E501
        """List transactions  # noqa: E501

        Returns budget transactions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions(budget_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param date since_date: Only return transactions on or after this date.
        :param str type: Only return transactions of a certain type (i.e. 'uncategorized', 'unapproved')
        :return: TransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_transactions_with_http_info(budget_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transactions_with_http_info(budget_id, **kwargs)  # noqa: E501
            return data

    def get_transactions_with_http_info(self, budget_id, **kwargs):  # noqa: E501
        """List transactions  # noqa: E501

        Returns budget transactions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_with_http_info(budget_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param date since_date: Only return transactions on or after this date.
        :param str type: Only return transactions of a certain type (i.e. 'uncategorized', 'unapproved')
        :return: TransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'since_date', 'type']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transactions" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `get_transactions`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501

        query_params = []
        if 'since_date' in params:
            query_params.append(('since_date', params['since_date']))  # noqa: E501
        if 'type' in params:
            query_params.append(('type', params['type']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transactions_by_account(self, budget_id, account_id, **kwargs):  # noqa: E501
        """List account transactions  # noqa: E501

        Returns all transactions for a specified account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_by_account(budget_id, account_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str account_id: The ID of the Account. (required)
        :param date since_date: Only return transactions on or after this date.
        :return: TransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_transactions_by_account_with_http_info(budget_id, account_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transactions_by_account_with_http_info(budget_id, account_id, **kwargs)  # noqa: E501
            return data

    def get_transactions_by_account_with_http_info(self, budget_id, account_id, **kwargs):  # noqa: E501
        """List account transactions  # noqa: E501

        Returns all transactions for a specified account  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_by_account_with_http_info(budget_id, account_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str account_id: The ID of the Account. (required)
        :param date since_date: Only return transactions on or after this date.
        :return: TransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'account_id', 'since_date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transactions_by_account" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `get_transactions_by_account`")  # noqa: E501
        # verify the required parameter 'account_id' is set
        if ('account_id' not in params or
                params['account_id'] is None):
            raise ValueError("Missing the required parameter `account_id` when calling `get_transactions_by_account`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501
        if 'account_id' in params:
            path_params['account_id'] = params['account_id']  # noqa: E501

        query_params = []
        if 'since_date' in params:
            query_params.append(('since_date', params['since_date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/accounts/{account_id}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transactions_by_category(self, budget_id, category_id, **kwargs):  # noqa: E501
        """List category transactions  # noqa: E501

        Returns all transactions for a specified category  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_by_category(budget_id, category_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str category_id: The ID of the Category. (required)
        :param date since_date: Only return transactions on or after this date.
        :return: TransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_transactions_by_category_with_http_info(budget_id, category_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transactions_by_category_with_http_info(budget_id, category_id, **kwargs)  # noqa: E501
            return data

    def get_transactions_by_category_with_http_info(self, budget_id, category_id, **kwargs):  # noqa: E501
        """List category transactions  # noqa: E501

        Returns all transactions for a specified category  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_by_category_with_http_info(budget_id, category_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str category_id: The ID of the Category. (required)
        :param date since_date: Only return transactions on or after this date.
        :return: TransactionsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'category_id', 'since_date']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transactions_by_category" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `get_transactions_by_category`")  # noqa: E501
        # verify the required parameter 'category_id' is set
        if ('category_id' not in params or
                params['category_id'] is None):
            raise ValueError("Missing the required parameter `category_id` when calling `get_transactions_by_category`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501
        if 'category_id' in params:
            path_params['category_id'] = params['category_id']  # noqa: E501

        query_params = []
        if 'since_date' in params:
            query_params.append(('since_date', params['since_date']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/categories/{category_id}/transactions', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def get_transactions_by_id(self, budget_id, transaction_id, **kwargs):  # noqa: E501
        """Single transaction  # noqa: E501

        Returns a single transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_by_id(budget_id, transaction_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str transaction_id: The ID of the Transaction. (required)
        :return: TransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.get_transactions_by_id_with_http_info(budget_id, transaction_id, **kwargs)  # noqa: E501
        else:
            (data) = self.get_transactions_by_id_with_http_info(budget_id, transaction_id, **kwargs)  # noqa: E501
            return data

    def get_transactions_by_id_with_http_info(self, budget_id, transaction_id, **kwargs):  # noqa: E501
        """Single transaction  # noqa: E501

        Returns a single transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.get_transactions_by_id_with_http_info(budget_id, transaction_id, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str transaction_id: The ID of the Transaction. (required)
        :return: TransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'transaction_id']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_transactions_by_id" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `get_transactions_by_id`")  # noqa: E501
        # verify the required parameter 'transaction_id' is set
        if ('transaction_id' not in params or
                params['transaction_id'] is None):
            raise ValueError("Missing the required parameter `transaction_id` when calling `get_transactions_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501
        if 'transaction_id' in params:
            path_params['transaction_id'] = params['transaction_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/transactions/{transaction_id}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)

    def update_transaction(self, budget_id, transaction_id, transaction, **kwargs):  # noqa: E501
        """Updates an existing transaction  # noqa: E501

        Updates a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.update_transaction(budget_id, transaction_id, transaction, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str transaction_id: The ID of the Transaction. (required)
        :param SaveTransactionWrapper transaction: The Transaction to update. (required)
        :return: TransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async'):
            return self.update_transaction_with_http_info(budget_id, transaction_id, transaction, **kwargs)  # noqa: E501
        else:
            (data) = self.update_transaction_with_http_info(budget_id, transaction_id, transaction, **kwargs)  # noqa: E501
            return data

    def update_transaction_with_http_info(self, budget_id, transaction_id, transaction, **kwargs):  # noqa: E501
        """Updates an existing transaction  # noqa: E501

        Updates a transaction  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async=True
        >>> thread = api.update_transaction_with_http_info(budget_id, transaction_id, transaction, async=True)
        >>> result = thread.get()

        :param async bool
        :param str budget_id: The ID of the Budget. (required)
        :param str transaction_id: The ID of the Transaction. (required)
        :param SaveTransactionWrapper transaction: The Transaction to update. (required)
        :return: TransactionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['budget_id', 'transaction_id', 'transaction']  # noqa: E501
        all_params.append('async')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method update_transaction" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'budget_id' is set
        if ('budget_id' not in params or
                params['budget_id'] is None):
            raise ValueError("Missing the required parameter `budget_id` when calling `update_transaction`")  # noqa: E501
        # verify the required parameter 'transaction_id' is set
        if ('transaction_id' not in params or
                params['transaction_id'] is None):
            raise ValueError("Missing the required parameter `transaction_id` when calling `update_transaction`")  # noqa: E501
        # verify the required parameter 'transaction' is set
        if ('transaction' not in params or
                params['transaction'] is None):
            raise ValueError("Missing the required parameter `transaction` when calling `update_transaction`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'budget_id' in params:
            path_params['budget_id'] = params['budget_id']  # noqa: E501
        if 'transaction_id' in params:
            path_params['transaction_id'] = params['transaction_id']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'transaction' in params:
            body_params = params['transaction']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearer']  # noqa: E501

        return self.api_client.call_api(
            '/budgets/{budget_id}/transactions/{transaction_id}', 'PUT',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='TransactionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async=params.get('async'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
