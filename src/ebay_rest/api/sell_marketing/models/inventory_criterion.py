# coding: utf-8

"""
    Marketing API

    <p>The <i>Marketing API </i> offers two platforms that sellers can use to promote and advertise their products:</p> <ul><li><b>Promoted Listings</b> is an eBay ad service that lets sellers set up <i>ad campaigns </i> for the products they want to promote. eBay displays the ads in search results and in other marketing modules as <b>SPONSORED</b> listings. If an item in a Promoted Listings campaign sells, the seller is assessed a Promoted Listings fee, which is a seller-specified percentage applied to the sales price. For complete details, refer to the <a href=\"/api-docs/sell/static/marketing/pl-landing.html\">Promoted Listings playbook</a>.</li><li><b>Promotions Manager</b> gives sellers a way to offer discounts on specific items as a way to attract buyers to their inventory. Sellers can set up discounts (such as \"20% off\" and other types of offers) on specific items or on an entire customer order. To further attract buyers, eBay prominently displays promotion <i>teasers</i> throughout buyer flows. For complete details, see <a href=\"/api-docs/sell/static/marketing/promotions-manager.html\">Promotions Manager</a>.</li></ul>  <p><b>Marketing reports</b>, on both the Promoted Listings and Promotions Manager platforms, give sellers information that shows the effectiveness of their marketing strategies. The data gives sellers the ability to review and fine tune their marketing efforts.</p><p><b>Store Email Campaign</b> allows sellers to create and send email campaigns to customers who have signed up to receive their newsletter. For more information on email campaigns, see <a href=\"/api-docs/sell/static/marketing/store-email-campaigns.html#email-campain-types\" target=\"_blank\">Store Email Campaigns</a>.<p class=\"tablenote\"><b>Important!</b> Sellers must have an active eBay Store subscription, and they must accept the <b>Terms and Conditions</b> before they can make requests to these APIs in the Production environment. There are also site-specific listings requirements and restrictions associated with these marketing tools, as listed in the \"requirements and restrictions\" sections for <a href=\"/api-docs/sell/marketing/static/overview.html#PL-requirements\">Promoted Listings</a> and <a href=\"/api-docs/sell/marketing/static/overview.html#PM-requirements\">Promotions Manager</a>.</p> <p>The table below lists all the Marketing API calls grouped by resource.</p>  # noqa: E501

    OpenAPI spec version: v1.22.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InventoryCriterion(object):
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
        'inventory_criterion_type': 'str',
        'inventory_items': 'list[InventoryItem]',
        'listing_ids': 'list[str]',
        'rule_criteria': 'RuleCriteria'
    }

    attribute_map = {
        'inventory_criterion_type': 'inventoryCriterionType',
        'inventory_items': 'inventoryItems',
        'listing_ids': 'listingIds',
        'rule_criteria': 'ruleCriteria'
    }

    def __init__(self, inventory_criterion_type=None, inventory_items=None, listing_ids=None, rule_criteria=None):  # noqa: E501
        """InventoryCriterion - a model defined in Swagger"""  # noqa: E501
        self._inventory_criterion_type = None
        self._inventory_items = None
        self._listing_ids = None
        self._rule_criteria = None
        self.discriminator = None
        if inventory_criterion_type is not None:
            self.inventory_criterion_type = inventory_criterion_type
        if inventory_items is not None:
            self.inventory_items = inventory_items
        if listing_ids is not None:
            self.listing_ids = listing_ids
        if rule_criteria is not None:
            self.rule_criteria = rule_criteria

    @property
    def inventory_criterion_type(self):
        """Gets the inventory_criterion_type of this InventoryCriterion.  # noqa: E501

        Indicates how the items to be discounted are selected. You can include inventory by ID, using rules, or globally include all your inventory.  For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/marketing/types/sme:InventoryCriterionEnum'>eBay API documentation</a>  # noqa: E501

        :return: The inventory_criterion_type of this InventoryCriterion.  # noqa: E501
        :rtype: str
        """
        return self._inventory_criterion_type

    @inventory_criterion_type.setter
    def inventory_criterion_type(self, inventory_criterion_type):
        """Sets the inventory_criterion_type of this InventoryCriterion.

        Indicates how the items to be discounted are selected. You can include inventory by ID, using rules, or globally include all your inventory.  For implementation help, refer to <a href='https://developer.ebay.com/api-docs/sell/marketing/types/sme:InventoryCriterionEnum'>eBay API documentation</a>  # noqa: E501

        :param inventory_criterion_type: The inventory_criterion_type of this InventoryCriterion.  # noqa: E501
        :type: str
        """

        self._inventory_criterion_type = inventory_criterion_type

    @property
    def inventory_items(self):
        """Gets the inventory_items of this InventoryCriterion.  # noqa: E501

        An array of containers for the seller's inventory reference IDs (also known as an \"SKU\" or \"custom label\") to be added to the discount.<br><p class=\"tablenote\"><b>Note:</b> The request can have either <b>inventoryItems</b> or <b>listingIds</b>, but not both.</p><br><b>Maximum:</b> 2000 parent items <br><br><b>Maximum SKU or custom label length:</b> 50 characters <br><br><i>Required if</i> <b>InventoryCriterionType</b> is set to <code>INVENTORY_BY_VALUE</code>, you must specify either <b>inventoryItems</b> or <b>listingIds</b>.  # noqa: E501

        :return: The inventory_items of this InventoryCriterion.  # noqa: E501
        :rtype: list[InventoryItem]
        """
        return self._inventory_items

    @inventory_items.setter
    def inventory_items(self, inventory_items):
        """Sets the inventory_items of this InventoryCriterion.

        An array of containers for the seller's inventory reference IDs (also known as an \"SKU\" or \"custom label\") to be added to the discount.<br><p class=\"tablenote\"><b>Note:</b> The request can have either <b>inventoryItems</b> or <b>listingIds</b>, but not both.</p><br><b>Maximum:</b> 2000 parent items <br><br><b>Maximum SKU or custom label length:</b> 50 characters <br><br><i>Required if</i> <b>InventoryCriterionType</b> is set to <code>INVENTORY_BY_VALUE</code>, you must specify either <b>inventoryItems</b> or <b>listingIds</b>.  # noqa: E501

        :param inventory_items: The inventory_items of this InventoryCriterion.  # noqa: E501
        :type: list[InventoryItem]
        """

        self._inventory_items = inventory_items

    @property
    def listing_ids(self):
        """Gets the listing_ids of this InventoryCriterion.  # noqa: E501

        An array of eBay listing IDs to be discounted. <br><p class=\"tablenote\"><b>Note:</b> The request can have either <b>inventoryItems</b> or <b>listingIds</b>, but not both.</p>  <br><b>Required:</b> All listings being discounted must offer an electronic payment method.<br><br><b>Maximum:</b> 2000 parent items <br><br><b>Maximum SKU or custom label length:</b> 50 characters <br><br><i>Required if</i> <b>InventoryCriterionType</b> is set to <code>INVENTORY_BY_VALUE</code>, you must specify either <b>inventoryItems</b> or <b>listingIds</b>.  # noqa: E501

        :return: The listing_ids of this InventoryCriterion.  # noqa: E501
        :rtype: list[str]
        """
        return self._listing_ids

    @listing_ids.setter
    def listing_ids(self, listing_ids):
        """Sets the listing_ids of this InventoryCriterion.

        An array of eBay listing IDs to be discounted. <br><p class=\"tablenote\"><b>Note:</b> The request can have either <b>inventoryItems</b> or <b>listingIds</b>, but not both.</p>  <br><b>Required:</b> All listings being discounted must offer an electronic payment method.<br><br><b>Maximum:</b> 2000 parent items <br><br><b>Maximum SKU or custom label length:</b> 50 characters <br><br><i>Required if</i> <b>InventoryCriterionType</b> is set to <code>INVENTORY_BY_VALUE</code>, you must specify either <b>inventoryItems</b> or <b>listingIds</b>.  # noqa: E501

        :param listing_ids: The listing_ids of this InventoryCriterion.  # noqa: E501
        :type: list[str]
        """

        self._listing_ids = listing_ids

    @property
    def rule_criteria(self):
        """Gets the rule_criteria of this InventoryCriterion.  # noqa: E501


        :return: The rule_criteria of this InventoryCriterion.  # noqa: E501
        :rtype: RuleCriteria
        """
        return self._rule_criteria

    @rule_criteria.setter
    def rule_criteria(self, rule_criteria):
        """Sets the rule_criteria of this InventoryCriterion.


        :param rule_criteria: The rule_criteria of this InventoryCriterion.  # noqa: E501
        :type: RuleCriteria
        """

        self._rule_criteria = rule_criteria

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
        if issubclass(InventoryCriterion, dict):
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
        if not isinstance(other, InventoryCriterion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
