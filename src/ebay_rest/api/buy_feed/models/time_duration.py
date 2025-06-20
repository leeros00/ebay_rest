# coding: utf-8

"""
    Buy Feed API

    The Feed API provides the ability to download TSV_GZIP feed files containing eBay items and an hourly snapshot file for a specific category, date, and marketplace.<br /><br />In addition to the API, there is an open-source Feed SDK written in Java that downloads, combines files into a single file when needed, and unzips the entire feed file. It also lets you specify field filters to curate the items in the file.  # noqa: E501

    OpenAPI spec version: v1.2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TimeDuration(object):
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
        'unit': 'str',
        'value': 'int'
    }

    attribute_map = {
        'unit': 'unit',
        'value': 'value'
    }

    def __init__(self, unit=None, value=None):  # noqa: E501
        """TimeDuration - a model defined in Swagger"""  # noqa: E501
        self._unit = None
        self._value = None
        self.discriminator = None
        if unit is not None:
            self.unit = unit
        if value is not None:
            self.value = value

    @property
    def unit(self):
        """Gets the unit of this TimeDuration.  # noqa: E501

        This enumeration value indicates the time unit used for the time period. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/feed/types/bas:TimeDurationUnitEnum'>eBay API documentation</a>  # noqa: E501

        :return: The unit of this TimeDuration.  # noqa: E501
        :rtype: str
        """
        return self._unit

    @unit.setter
    def unit(self, unit):
        """Sets the unit of this TimeDuration.

        This enumeration value indicates the time unit used for the time period. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/buy/feed/types/bas:TimeDurationUnitEnum'>eBay API documentation</a>  # noqa: E501

        :param unit: The unit of this TimeDuration.  # noqa: E501
        :type: str
        """

        self._unit = unit

    @property
    def value(self):
        """Gets the value of this TimeDuration.  # noqa: E501

        The number of units of time in the span.  # noqa: E501

        :return: The value of this TimeDuration.  # noqa: E501
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this TimeDuration.

        The number of units of time in the span.  # noqa: E501

        :param value: The value of this TimeDuration.  # noqa: E501
        :type: int
        """

        self._value = value

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
        if issubclass(TimeDuration, dict):
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
        if not isinstance(other, TimeDuration):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
