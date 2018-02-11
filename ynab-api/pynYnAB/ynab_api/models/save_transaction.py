# coding: utf-8

"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class SaveTransaction(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'account_id': 'str',
        'date': 'date',
        'amount': 'float',
        'cleared': 'str',
        'approved': 'bool'
    }

    attribute_map = {
        'account_id': 'account_id',
        'date': 'date',
        'amount': 'amount',
        'cleared': 'cleared',
        'approved': 'approved'
    }

    def __init__(self, account_id=None, date=None, amount=None, cleared=None, approved=None):  # noqa: E501
        """SaveTransaction - a model defined in Swagger"""  # noqa: E501

        self._account_id = None
        self._date = None
        self._amount = None
        self._cleared = None
        self._approved = None
        self.discriminator = None

        self.account_id = account_id
        self.date = date
        self.amount = amount
        if cleared is not None:
            self.cleared = cleared
        if approved is not None:
            self.approved = approved

    @property
    def account_id(self):
        """Gets the account_id of this SaveTransaction.  # noqa: E501


        :return: The account_id of this SaveTransaction.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this SaveTransaction.


        :param account_id: The account_id of this SaveTransaction.  # noqa: E501
        :type: str
        """
        if account_id is None:
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def date(self):
        """Gets the date of this SaveTransaction.  # noqa: E501


        :return: The date of this SaveTransaction.  # noqa: E501
        :rtype: date
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this SaveTransaction.


        :param date: The date of this SaveTransaction.  # noqa: E501
        :type: date
        """
        if date is None:
            raise ValueError("Invalid value for `date`, must not be `None`")  # noqa: E501

        self._date = date

    @property
    def amount(self):
        """Gets the amount of this SaveTransaction.  # noqa: E501

        The transaction amount in milliunits format  # noqa: E501

        :return: The amount of this SaveTransaction.  # noqa: E501
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount):
        """Sets the amount of this SaveTransaction.

        The transaction amount in milliunits format  # noqa: E501

        :param amount: The amount of this SaveTransaction.  # noqa: E501
        :type: float
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount

    @property
    def cleared(self):
        """Gets the cleared of this SaveTransaction.  # noqa: E501

        The cleared status of the transaction  # noqa: E501

        :return: The cleared of this SaveTransaction.  # noqa: E501
        :rtype: str
        """
        return self._cleared

    @cleared.setter
    def cleared(self, cleared):
        """Sets the cleared of this SaveTransaction.

        The cleared status of the transaction  # noqa: E501

        :param cleared: The cleared of this SaveTransaction.  # noqa: E501
        :type: str
        """
        allowed_values = ["Cleared", "Uncleared", "Reconciled"]  # noqa: E501
        if cleared not in allowed_values:
            raise ValueError(
                "Invalid value for `cleared` ({0}), must be one of {1}"  # noqa: E501
                .format(cleared, allowed_values)
            )

        self._cleared = cleared

    @property
    def approved(self):
        """Gets the approved of this SaveTransaction.  # noqa: E501

        Whether or not the transaction is approved.  If not supplied, transaction will be unapproved by default.  # noqa: E501

        :return: The approved of this SaveTransaction.  # noqa: E501
        :rtype: bool
        """
        return self._approved

    @approved.setter
    def approved(self, approved):
        """Sets the approved of this SaveTransaction.

        Whether or not the transaction is approved.  If not supplied, transaction will be unapproved by default.  # noqa: E501

        :param approved: The approved of this SaveTransaction.  # noqa: E501
        :type: bool
        """

        self._approved = approved

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SaveTransaction):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other