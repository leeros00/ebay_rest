# coding: utf-8

"""
    Metadata API

    The Metadata API has operations that retrieve configuration details pertaining to the different eBay marketplaces. In addition to marketplace information, the API also has operations that get information that helps sellers list items on eBay.  # noqa: E501

    OpenAPI spec version: v1.11.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Compatibility(object):
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
        'compatibility_details': 'list[CompatibilityDetails]'
    }

    attribute_map = {
        'compatibility_details': 'compatibilityDetails'
    }

    def __init__(self, compatibility_details=None):  # noqa: E501
        """Compatibility - a model defined in Swagger"""  # noqa: E501
        self._compatibility_details = None
        self.discriminator = None
        if compatibility_details is not None:
            self.compatibility_details = compatibility_details

    @property
    def compatibility_details(self):
        """Gets the compatibility_details of this Compatibility.  # noqa: E501

        This array returns a list of compatibility details associated with the specified property name(s).  # noqa: E501

        :return: The compatibility_details of this Compatibility.  # noqa: E501
        :rtype: list[CompatibilityDetails]
        """
        return self._compatibility_details

    @compatibility_details.setter
    def compatibility_details(self, compatibility_details):
        """Sets the compatibility_details of this Compatibility.

        This array returns a list of compatibility details associated with the specified property name(s).  # noqa: E501

        :param compatibility_details: The compatibility_details of this Compatibility.  # noqa: E501
        :type: list[CompatibilityDetails]
        """

        self._compatibility_details = compatibility_details

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
        if issubclass(Compatibility, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Compatibility):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
