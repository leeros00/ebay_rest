# coding: utf-8

"""
    Finances API

    This API is used to retrieve seller payouts and monetary transaction details related to those payouts.  # noqa: E501

    OpenAPI spec version: v1.17.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Amount(object):
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
        'converted_from_currency': 'str',
        'converted_from_value': 'str',
        'converted_to_currency': 'str',
        'converted_to_value': 'str',
        'currency': 'str',
        'exchange_rate': 'str',
        'value': 'str'
    }

    attribute_map = {
        'converted_from_currency': 'convertedFromCurrency',
        'converted_from_value': 'convertedFromValue',
        'converted_to_currency': 'convertedToCurrency',
        'converted_to_value': 'convertedToValue',
        'currency': 'currency',
        'exchange_rate': 'exchangeRate',
        'value': 'value'
    }

    def __init__(self, converted_from_currency=None, converted_from_value=None, converted_to_currency=None, converted_to_value=None, currency=None, exchange_rate=None, value=None):  # noqa: E501
        """Amount - a model defined in Swagger"""  # noqa: E501
        self._converted_from_currency = None
        self._converted_from_value = None
        self._converted_to_currency = None
        self._converted_to_value = None
        self._currency = None
        self._exchange_rate = None
        self._value = None
        self.discriminator = None
        if converted_from_currency is not None:
            self.converted_from_currency = converted_from_currency
        if converted_from_value is not None:
            self.converted_from_value = converted_from_value
        if converted_to_currency is not None:
            self.converted_to_currency = converted_to_currency
        if converted_to_value is not None:
            self.converted_to_value = converted_to_value
        if currency is not None:
            self.currency = currency
        if exchange_rate is not None:
            self.exchange_rate = exchange_rate
        if value is not None:
            self.value = value

    @property
    def converted_from_currency(self):
        """Gets the converted_from_currency of this Amount.  # noqa: E501

        The three-letter <a href=\"https://www.iso.org/iso-4217-currency-codes.html \" target=\"_blank\">ISO 4217</a> code representing the currency of the amount in the <b> convertedFromValue</b> field. This value is the pre-conversion currency.<br><br>This field is only returned if/when currency conversion was applied by eBay. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/finances/types/ba:CurrencyCodeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The converted_from_currency of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._converted_from_currency

    @converted_from_currency.setter
    def converted_from_currency(self, converted_from_currency):
        """Sets the converted_from_currency of this Amount.

        The three-letter <a href=\"https://www.iso.org/iso-4217-currency-codes.html \" target=\"_blank\">ISO 4217</a> code representing the currency of the amount in the <b> convertedFromValue</b> field. This value is the pre-conversion currency.<br><br>This field is only returned if/when currency conversion was applied by eBay. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/finances/types/ba:CurrencyCodeEnum'>eBay API documentation</a>  # noqa: E501

        :param converted_from_currency: The converted_from_currency of this Amount.  # noqa: E501
        :type: str
        """

        self._converted_from_currency = converted_from_currency

    @property
    def converted_from_value(self):
        """Gets the converted_from_value of this Amount.  # noqa: E501

        The monetary amount before any conversion is performed, in the currency specified by the <b> convertedFromCurrency</b> field. This value is the pre-conversion amount. The <b> value</b> field contains the converted amount of this value, in the currency specified by the <b> currency</b> field.<br><br>This field is only returned if/when currency conversion was applied by eBay.  # noqa: E501

        :return: The converted_from_value of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._converted_from_value

    @converted_from_value.setter
    def converted_from_value(self, converted_from_value):
        """Sets the converted_from_value of this Amount.

        The monetary amount before any conversion is performed, in the currency specified by the <b> convertedFromCurrency</b> field. This value is the pre-conversion amount. The <b> value</b> field contains the converted amount of this value, in the currency specified by the <b> currency</b> field.<br><br>This field is only returned if/when currency conversion was applied by eBay.  # noqa: E501

        :param converted_from_value: The converted_from_value of this Amount.  # noqa: E501
        :type: str
        """

        self._converted_from_value = converted_from_value

    @property
    def converted_to_currency(self):
        """Gets the converted_to_currency of this Amount.  # noqa: E501

        <span class=\"tablenote\"><b>Note:</b> This field is only applicable for Mainland China sellers with an available CNY Bank payment instrument. This response can <b>only</b> have a value of <code>CNY</code>.</span>The three-letter <a href=\"https://www.iso.org/iso-4217-currency-codes.html \" target=\"_blank\">ISO 4217</a> code representing the currency of the amount in the <b>convertedToValue</b> field. <br/><br/>This field is only returned for payouts to bank accounts when currency conversion was applied by eBay. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/finances/types/ba:CurrencyCodeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The converted_to_currency of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._converted_to_currency

    @converted_to_currency.setter
    def converted_to_currency(self, converted_to_currency):
        """Sets the converted_to_currency of this Amount.

        <span class=\"tablenote\"><b>Note:</b> This field is only applicable for Mainland China sellers with an available CNY Bank payment instrument. This response can <b>only</b> have a value of <code>CNY</code>.</span>The three-letter <a href=\"https://www.iso.org/iso-4217-currency-codes.html \" target=\"_blank\">ISO 4217</a> code representing the currency of the amount in the <b>convertedToValue</b> field. <br/><br/>This field is only returned for payouts to bank accounts when currency conversion was applied by eBay. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/finances/types/ba:CurrencyCodeEnum'>eBay API documentation</a>  # noqa: E501

        :param converted_to_currency: The converted_to_currency of this Amount.  # noqa: E501
        :type: str
        """

        self._converted_to_currency = converted_to_currency

    @property
    def converted_to_value(self):
        """Gets the converted_to_value of this Amount.  # noqa: E501

        <span class=\"tablenote\"><b>Note:</b> This field is only applicable for Mainland China sellers with an available CNY Bank payment instrument. This response <b>only</b> returns value in CNY.</span>The monetary value after any conversion is performed, in the currency specified by the <b>convertedToCurrency</b> field. This value is the converted amount. <br/><br/>The field is only returned for payouts to bank accounts when currency conversion was applied by eBay.  # noqa: E501

        :return: The converted_to_value of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._converted_to_value

    @converted_to_value.setter
    def converted_to_value(self, converted_to_value):
        """Sets the converted_to_value of this Amount.

        <span class=\"tablenote\"><b>Note:</b> This field is only applicable for Mainland China sellers with an available CNY Bank payment instrument. This response <b>only</b> returns value in CNY.</span>The monetary value after any conversion is performed, in the currency specified by the <b>convertedToCurrency</b> field. This value is the converted amount. <br/><br/>The field is only returned for payouts to bank accounts when currency conversion was applied by eBay.  # noqa: E501

        :param converted_to_value: The converted_to_value of this Amount.  # noqa: E501
        :type: str
        """

        self._converted_to_value = converted_to_value

    @property
    def currency(self):
        """Gets the currency of this Amount.  # noqa: E501

        A three-letter ISO 4217 code that indicates the currency of the amount in the <b>value</b> field. This field is always returned with any container using <b>Amount</b> type. <br><br><b>Default</b>: The currency of the authenticated user's country. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/finances/types/ba:CurrencyCodeEnum'>eBay API documentation</a>  # noqa: E501

        :return: The currency of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._currency

    @currency.setter
    def currency(self, currency):
        """Sets the currency of this Amount.

        A three-letter ISO 4217 code that indicates the currency of the amount in the <b>value</b> field. This field is always returned with any container using <b>Amount</b> type. <br><br><b>Default</b>: The currency of the authenticated user's country. For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/finances/types/ba:CurrencyCodeEnum'>eBay API documentation</a>  # noqa: E501

        :param currency: The currency of this Amount.  # noqa: E501
        :type: str
        """

        self._currency = currency

    @property
    def exchange_rate(self):
        """Gets the exchange_rate of this Amount.  # noqa: E501

        The exchange rate used for the monetary conversion. This field shows the exchange rate used to convert the dollar value in the <b>value</b> field from the dollar value in the <b>convertedFromValue</b> field.<br><br> For sellers in mainland China, this field shows shows the exchange rate to convert the dollar value in the <b>value</b> field to the CNY value in the <b>convertedToValue</b> field.<br><br>This field is only returned when eBay does a currency version, and a currency conversion is generally needed if the buyer is viewing, or has purchased an item on an international site. <br><br>This field is only returned if/when currency conversion was applied by eBay.  # noqa: E501

        :return: The exchange_rate of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, exchange_rate):
        """Sets the exchange_rate of this Amount.

        The exchange rate used for the monetary conversion. This field shows the exchange rate used to convert the dollar value in the <b>value</b> field from the dollar value in the <b>convertedFromValue</b> field.<br><br> For sellers in mainland China, this field shows shows the exchange rate to convert the dollar value in the <b>value</b> field to the CNY value in the <b>convertedToValue</b> field.<br><br>This field is only returned when eBay does a currency version, and a currency conversion is generally needed if the buyer is viewing, or has purchased an item on an international site. <br><br>This field is only returned if/when currency conversion was applied by eBay.  # noqa: E501

        :param exchange_rate: The exchange_rate of this Amount.  # noqa: E501
        :type: str
        """

        self._exchange_rate = exchange_rate

    @property
    def value(self):
        """Gets the value of this Amount.  # noqa: E501

        The monetary amount, in the currency specified by the <b>currency</b> field. This field is always returned with any container using <b>Amount</b> type.  # noqa: E501

        :return: The value of this Amount.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this Amount.

        The monetary amount, in the currency specified by the <b>currency</b> field. This field is always returned with any container using <b>Amount</b> type.  # noqa: E501

        :param value: The value of this Amount.  # noqa: E501
        :type: str
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
        if issubclass(Amount, dict):
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
        if not isinstance(other, Amount):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
