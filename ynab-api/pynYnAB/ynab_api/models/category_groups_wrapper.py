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

from pynYnAB.ynab_api.models.category_group_with_categories import CategoryGroupWithCategories  # noqa: F401,E501


class CategoryGroupsWrapper(object):
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
        'category_groups': 'list[CategoryGroupWithCategories]'
    }

    attribute_map = {
        'category_groups': 'category_groups'
    }

    def __init__(self, category_groups=None):  # noqa: E501
        """CategoryGroupsWrapper - a model defined in Swagger"""  # noqa: E501

        self._category_groups = None
        self.discriminator = None

        self.category_groups = category_groups

    @property
    def category_groups(self):
        """Gets the category_groups of this CategoryGroupsWrapper.  # noqa: E501


        :return: The category_groups of this CategoryGroupsWrapper.  # noqa: E501
        :rtype: list[CategoryGroupWithCategories]
        """
        return self._category_groups

    @category_groups.setter
    def category_groups(self, category_groups):
        """Sets the category_groups of this CategoryGroupsWrapper.


        :param category_groups: The category_groups of this CategoryGroupsWrapper.  # noqa: E501
        :type: list[CategoryGroupWithCategories]
        """
        if category_groups is None:
            raise ValueError("Invalid value for `category_groups`, must not be `None`")  # noqa: E501

        self._category_groups = category_groups

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
        if not isinstance(other, CategoryGroupsWrapper):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
