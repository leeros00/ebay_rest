# *** A way to run these unit tests. ***
# 1. (Open a terminal, alternately known as go to the command line.)
# 2. cd .. (Or, somehow make the project root the current directory.)
# 3. python -m unittest tests.ebay_rest

# Don't repeat API calls with the same parameters, because it appears to trigger an "Internal (Server) Error" at eBay.

# Whenever possible, run tests on the sandbox instead of production.

# Standard library imports
import datetime
import os
import random
import string
from json import loads
import unittest
import warnings

# 3rd party libraries
from currency_converter import CurrencyConverter

# Local imports
from src.ebay_rest import API, DateTime, Error, Reference


class APIBothEnvironmentsSingleSiteTests(unittest.TestCase):
    def test_start(
        self,
    ):
        try:
            # all initialization options and for each the first and second usage
            for environment in ("production", "sandbox"):
                for throttle, timeout in ((False, None), (True, None), (True, 60.0)):

                    if timeout is None:
                        api = API(
                            application=environment + "_1",
                            user=environment + "_1",
                            header="US",
                            throttle=throttle,
                        )
                    else:
                        api = API(
                            application=environment + "_1",
                            user=environment + "_1",
                            header="US",
                            throttle=throttle,
                            timeout=timeout,
                        )
                    item_id = None
                    for record in api.buy_browse_search(limit=1, q="lego"):
                        if "record" not in record:
                            self.assertTrue(
                                "total" in record, f"Unexpected non-record{record}."
                            )
                        else:
                            item = record["record"]
                            self.assertTrue(isinstance(item["item_id"], str))
                            item_id = item["item_id"]
                            break
                    if item_id:
                        item = api.buy_browse_get_item(item_id=item_id)
                        self.assertTrue(isinstance(item, dict))
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")


class APISandboxMultipleSiteTests(unittest.TestCase):
    """API test that require multiple marketplaces and that can be done on the sandbox."""

    @classmethod
    def setUpClass(cls):
        cls.currency_converter = CurrencyConverter()  # this is slow, so do it once

    def test_credentials_from_dicts(self):
        """set credentials via dicts"""
        config_location = os.path.join(os.getcwd(), "ebay_rest.json")
        try:
            f = open(config_location, "r")
        except FileNotFoundError:
            self.fail(f"File not found, unable to open {config_location}.")
        else:
            try:
                contents = loads(f.read())
            except IOError:
                f.close()
                self.fail(
                    f"Unable to load the file {config_location}; likely the json is malformed."
                )
            else:
                f.close()

                application = None
                if "applications" in contents:
                    if "sandbox_1" in contents["applications"]:
                        application = contents["applications"]["sandbox_1"]
                self.assertIsInstance(
                    application, dict, "Failed to load application credentials."
                )

                user = None
                if "users" in contents:
                    if "sandbox_1" in contents["users"]:
                        user = contents["users"]["sandbox_1"]
                self.assertIsInstance(user, dict, "Failed to load user credentials.")

                header = None
                if "headers" in contents:
                    if "US" in contents["headers"]:
                        header = contents["headers"]["US"]
                self.assertIsInstance(
                    header, dict, "Failed to load header credentials."
                )

                try:
                    api = API(
                        application=application, user=user, header=header
                    )  # params are dicts
                except Error as error:
                    self.fail(
                        f"Error {error.number} is {error.reason}  {error.detail}.\n"
                    )
                else:
                    # Ignore the PyCharm linter bug
                    # 'Expected type 'Union[type, Tuple[type, ...]]', got 'Multiton' instead'
                    self.assertIsInstance(api, API, "An API object was not returned.")  # type: ignore

    def test_object_reuse(self):
        """Do the same parameters return the same API object?"""
        a1 = API(application="sandbox_1", user="sandbox_1", header="ENCA")
        a2 = API(application="sandbox_1", user="sandbox_1", header="ENCA")
        b = API(application="sandbox_1", user="sandbox_1", header="GB")
        self.assertEqual(a1, a2)
        self.assertNotEqual(a1, b)

    def test_credential_path(self):
        """supply a path to ebay_rest.json"""
        try:
            api = API(
                path=os.getcwd(), application="sandbox_1", user="sandbox_1", header="US"
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            # Ignore the PyCharm linter bug 'Expected type 'Union[type, Tuple[type, ...]]', got 'Multiton' instead'
            self.assertIsInstance(api, API, "An API object was not returned.")  # type: ignore

    def test_shipping_accuracy(self):
        """Is closer shipping cheaper?"""

        # domestic
        # d_market = 'EBAY_ENCA'    # set in header
        d_country = "CA"
        d_currency = "CAD"
        # d_zip = 'K1M 1M4'         # set in header

        # foreign
        # f_market = 'EBAY_GB'      # set in header
        f_country = "GB"
        # f_currency = 'GBP'
        # f_zip = 'SW1A 1AA'        # set in header

        # more constants
        shipping_currency = "USD"

        tally = 0  # how many times domestic shipping is cheaper than foreign

        d_api = API(application="production_1", user="production_1", header="ENCA")
        f_api = API(application="production_1", user="production_1", header="GB")

        # in the local marketplace find items located locally that also ship to foreign
        # low-priced items are targeted because free shipping for them is unlikely
        # black items are targeted because they are plentiful, and the q parameter is mandatory
        try:
            filter_ = (
                f"deliveryCountry:{f_country},itemLocationCountry:{d_country},price:[1..2],"
                f"priceCurrency:{d_currency} "
            )

            for record in d_api.buy_browse_search(q="black", filter=filter_, limit=10):
                if "record" not in record:
                    self.assertTrue(
                        "total" in record, f"Unexpected non-record{record}."
                    )
                else:
                    item = record["record"]
                    item_id = item["item_id"]
                    if item["item_location"]["country"] == d_country:
                        # get the lowest domestic shipping cost
                        try:
                            d_item = d_api.buy_browse_get_item(
                                item_id=item_id, fieldgroups="PRODUCT"
                            )
                        except Error as error:
                            self.fail(
                                f"Error {error.number} is {error.reason}  {error.detail}.\n"
                            )
                        d_shipping = self._get_lowest_shipping(
                            d_item, d_country, shipping_currency
                        )

                        # get the lowest foreign shipping cost
                        try:
                            f_item = f_api.buy_browse_get_item(
                                item_id=item_id, fieldgroups="PRODUCT"
                            )
                        except Error as error:
                            self.fail(
                                f"Error {error.number} is {error.reason}  {error.detail}.\n"
                            )
                        f_shipping = self._get_lowest_shipping(
                            f_item, f_country, shipping_currency
                        )

                        # compare costs, inconclusive when equal or some None
                        if (d_shipping is not None) and (f_shipping is not None):
                            if d_shipping < f_shipping:
                                tally += 1  # what we would expect most of the time
                            elif d_shipping > f_shipping:
                                tally -= (
                                    1  # very rare, put a break point here find trouble
                                )
                            else:
                                tally = (
                                    tally  # flat rate worldwide shipping is possible
                                )
                        else:
                            pass  # self.fail(f"For {item_id} both shipping costs can not be found.")
                    else:
                        self.fail(
                            f"Item {item_id} is supposed to be located in {d_country}."
                        )

        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")

        self.assertTrue(tally > 0, "Domestic shipping should cost less than foreign.")

    def _get_lowest_shipping(self, item: dict, country: str, currency: str):
        costs = []

        # is shipping excluded?
        ship_to_locations = item["ship_to_locations"]
        if ship_to_locations:
            if self._in_region(ship_to_locations["region_excluded"] or [], country):
                return None
            # if not in either list, then eBay concludes that shipping is allowed, so skip the following
            # elif not self._in_region(ship_to_locations['region_included'], country):
            # return None

        # find all costs
        if not item["shipping_options"]:
            return None
        for shipping_option in item["shipping_options"]:
            shipping_cost = shipping_option["shipping_cost"]
            if shipping_cost["currency"] == currency:
                cost = float(shipping_cost["value"])
            elif shipping_cost["converted_from_currency"] == currency:
                cost = float(shipping_cost["converted_from_value"])
            else:
                cost = self.currency_converter.convert(
                    float(shipping_cost["value"]), shipping_cost["currency"], currency
                )
            if cost is not None:
                costs.append(cost)
            else:
                self.fail("A shipping cost, without a cost, should not be possible.")

        if costs:
            costs.sort()
            return costs[0]
        else:
            self.fail("Shipping options without any options, should not be possible.")

    def _in_region(self, regions: dict, country: str):
        if country in ("CA", "US"):
            region_ids = ("AMERICAS", "NORTH_AMERICA")
        elif country in ("GB",):
            region_ids = ("EUROPE",)
        else:
            self.fail("add region ids for your country")

        for region in regions:
            region_type = region["region_type"]
            if region_type == "COUNTRY":
                if region["region_id"] == country:
                    return True
            elif region_type == "WORLD_REGION":
                if region["region_id"] in region_ids:
                    return True
            elif region_type == "WORLDWIDE":
                return True
        return False


class APISandboxSingleSiteTests(unittest.TestCase):
    """API tests that can be done on a single marketplace and in the sandbox.
    Also, try the non-default option of making asynchronous HTTP requests.
    """

    @classmethod
    def setUpClass(cls):
        try:
            # TODO Change to async_req=True.
            cls._api = API(
                application="sandbox_1", user="sandbox_1", header="US", async_req=False
            )
        except Error as error:
            cls.number = error.number
            cls.reason = error.reason
            cls.detail = error.detail
        else:
            cls.number = None
        cls.marketplace_id = cls._api._header["marketplace_id"]

    def setUp(self):
        if self.number is not None:
            self.fail(f"Error {self.number} is {self.reason}  {self.detail}.\n")

    def test_paging_no_results(self):
        try:
            for record in self._api.buy_browse_search(
                q="atomic-donkey-kick--this-will-not-be-found-Geraldine"
            ):
                if "record" not in record:
                    self.assertTrue(
                        "total" in record, f"Unexpected non-record{record}."
                    )
                    self.assertEqual(record["total"]["records_yielded"], 0)
                    self.assertEqual(record["total"]["records_available"], 0)
                else:
                    item = record["record"]
                    self.assertTrue(isinstance(item["item_id"], str), "Malformed item.")
                    self.fail(msg="No items should be returned.")
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")

    def test_positional_none_kw_none(self):
        """Try a call with no positional arguments and no keyword arguments."""
        try:
            result = self._api.sell_compliance_get_listing_violations_summary(
                x_ebay_c_marketplace_id=self.marketplace_id
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            msg = "A call with zero positional and no kw arguments failed."
            self.assertIsNotNone("violation_summaries" in result, msg=msg)

    def test_positional_some_kw_none(self):
        # https://developer.ebay.com/api-docs/commerce/taxonomy/resources/category_tree/methods/getDefaultCategoryTreeId
        try:
            result = self._api.commerce_taxonomy_get_default_category_tree_id("EBAY_US")
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            self.assertTrue(
                "category_tree_id" in result,
                msg="A call with some positional and no kw arguments failed.",
            )

    def test_positional_none_kw_some(self):
        try:
            for record in self._api.buy_browse_search(q="red"):
                if "record" in record:
                    item = record["record"]
                    self.assertTrue(
                        "item_id" in item,
                        msg="A call with some positional and no kw arguments failed.",
                    )
                    break
                else:
                    self.assertTrue(
                        "total" in record, f"Unexpected non-record{record}."
                    )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")

    def test_positional_some_kw_some(self):
        # Redundant, several unit tests call buy_browse_search, so this test case is well covered.
        pass

    def test_try_except_else_api(self):
        """Test that an exception occurs when expected."""
        try:
            self._api.buy_browse_get_item(item_id="invalid")
        except Error as error:
            self.assertIsNotNone(
                f"Error {error.number} is {error.reason} with detail {error.detail}."
            )
        else:
            self.assertIsNotNone(None, msg="Failed to raise an exception.")

    def test_buying_options(self):
        """Does buying option filtering work?"""
        options = [
            "BEST_OFFER",
            "FIXED_PRICE",
        ]  # on Production 'AUCTION' and 'CLASSIFIED_AD' are also options
        for option in options:
            try:
                success = None
                keywords = "black"
                filter_ = "buyingOptions:{" + option + "}"
                for record in self._api.buy_browse_search(
                    q=keywords, filter=filter_, limit=500
                ):
                    if "record" not in record:
                        self.assertTrue(
                            "total" in record, f"Unexpected non-record{record}."
                        )
                    else:
                        item = record["record"]
                        if option in item["buying_options"]:
                            success = True
                        else:
                            success = False
                            break
            except Error as error:
                self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
            else:
                message = (
                    "The search for "
                    + option
                    + " items returned no items or a non-auction item."
                )
                self.assertTrue(success, message)

    def test_get_transaction_summary(self):
        """
        https://developer.ebay.com/api-docs/sell/finances/resources/transaction/methods/getTransactionSummary
        """
        try:
            result = self._api.sell_finances_get_transaction_summary(
                filter="transactionStatus:{PAYOUT}",
                x_ebay_c_marketplace_id=self.marketplace_id,
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            self.assertTrue("credit_count" in result)

    def test_sell_feed_create_inventory_task(self):
        """
        https://developer.ebay.com/api-docs/sell/feed/resources/inventory_task/methods/createInventoryTask

        The underlying REST call returns the new id in the header; which can't be gotten with the combination of Swagger
        and OpenAPI contract which we rely on here. A workaround uses a related call to retrieve task_id_new.
        """

        try:
            feed_type = "LMS_ACTIVE_INVENTORY_REPORT"
            body = {"schemaVersion": "1.0", "feedType": feed_type}
            task_ids_pre = self.get_task_ids(feed_type=feed_type)

            result = self._api.sell_feed_create_inventory_task(
                content_type="application/json", body=body
            )
            self.assertIsNone(
                result,
                "eBay made a change, the call now returns something, can the work around go?",
            )
            task_ids_post = self.get_task_ids(feed_type=feed_type)
            task_ids_new = task_ids_post.difference(task_ids_pre)
            self.assertEqual(
                1,
                len(task_ids_new),
                "In this test, one and only one task id is expected.",
            )
            # task_id_new = task_ids_new.pop()    # the new task id that we worked so hard to get

        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        except Exception as ex:
            self.fail(f"An unexpected error occurred: {str(ex)}")

    def get_task_ids(self, feed_type: string):
        """
        https://developer.ebay.com/api-docs/sell/feed/resources/inventory_task/methods/getInventoryTasks

        :param feed_type: (string)
        :return: task_ids (set(string))
        """
        task_ids = set()
        for record in self._api.sell_feed_get_inventory_tasks(
            feed_type=feed_type, look_back_days="1"
        ):
            if "record" in record:
                task_ids.add(record["record"]["task_id"])
            elif "total" in record:
                self.assertEqual(
                    record["total"]["records_yielded"],
                    record["total"]["records_available"],
                    "We missed some data - narrow the search!",
                )
            else:
                self.fail(f"unexpected record {record}")
        return task_ids


class APIProductionSingleTests(unittest.TestCase):
    """API tests that can be done on a single marketplace and must in be in system production."""

    @classmethod
    def setUpClass(cls):
        try:
            cls._api = API(application="production_1", user="production_1", header="US")
        except Error as error:
            cls.number = error.number
            cls.reason = error.reason
            cls.detail = error.detail
        else:
            cls.number = None

    def setUp(self):
        if self.number is not None:
            self.fail(f"Error {self.number} is {self.reason}  {self.detail}.\n")

    def test_hidden_page_boundaries(self):
        """
        Warning, this can't be run in the sandbox, because searches do not return enough results.
        """
        limit_and_keywords = (
            (
                1,
                "red",
            ),  # start at one because zero is not allowed
            (
                2,
                "orange",
            ),
            (
                198,
                "yellow",
            ),
            (
                199,
                "green",
            ),
            (
                200,
                "blue",
            ),  # the biggest page can hold 200 items
            (
                201,
                "indigo",
            ),
            (
                202,
                "violet",
            ),
        )
        for limit, keywords in limit_and_keywords:
            counter = 0
            safety = limit + 5
            for record in self._api.buy_browse_search(limit=limit, q=keywords):
                if "record" not in record:
                    self.assertTrue(
                        "total" in record, f"Unexpected non-record{record}."
                    )
                else:
                    item = record["record"]
                    self.assertTrue(isinstance(item["item_id"], str), "Malformed item.")
                    counter += 1
                    if counter >= safety:
                        break
            self.assertTrue(counter == limit, f"Page boundary error on limit {limit}.")

    def test_sell_inventory(self):
        """
        See https://developer.ebay.com/api-docs/sell/inventory/static/overview.html

        :return:
        """
        # A unique, merchant-defined key (ID) for an inventory location.
        # This unique identifier, or key, is used in other Inventory API calls to identify an inventory location.
        length = random.randint(1, 36)
        allowed = (
            string.ascii_letters + string.digits + "_" + "-"
        )  # more might be allowed, eBay's docs are unclear
        merchant_location_key = "".join(random.choice(allowed) for _i in range(length))

        # Create a new inventory location.
        # https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/createInventoryLocation
        # A template for supplying all possible information about a location.
        _body = {
            "location": {
                "address": {
                    "addressLine1": "string",
                    "addressLine2": "string",
                    "city": "string",
                    "country": "CountryCodeEnum",
                    "county": "string",
                    "postalCode": "string",
                    "stateOrProvince": "string",
                },
                "geoCoordinates": {"latitude": "number", "longitude": "number"},
            },
            "locationAdditionalInformation": "string",
            "locationInstructions": "string",
            "locationTypes": ["StoreTypeEnum"],
            "locationWebUrl": "string",
            "merchantLocationStatus": "StatusEnum : [DISABLED,ENABLED]",
            "name": "string",
            "operatingHours": [
                {
                    "dayOfWeekEnum": "DayOfWeekEnum : [MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY]",
                    "intervals": [{"close": "string", "open": "string"}],
                }
            ],
            "phone": "string",
            "specialHours": [
                {"date": "string", "intervals": [{"close": "string", "open": "string"}]}
            ],
        }
        # A template for supplying the bare minimum about a location.
        body = {
            "location": {
                "address": {
                    "addressLine1": "2********e",
                    "addressLine2": "B********3",
                    "city": "S*****e",
                    "stateOrProvince": "**",
                    "postalCode": "9***5",
                    "country": "US",
                }
            },
            "locationInstructions": "Items ship from here.",
            "name": "W********1",
            "merchantLocationStatus": "ENABLED",
            "locationTypes": ["WAREHOUSE"],
        }
        try:
            self._api.sell_inventory_create_inventory_location(
                content_type="application/json",
                body=body,
                merchant_location_key=merchant_location_key,
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")

        # Confirm the new location.
        # https://developer.ebay.com/api-docs/sell/inventory/resources/location/methods/getInventoryLocations
        confirmed = False
        try:
            for record in self._api.sell_inventory_get_inventory_locations():
                if "record" not in record:
                    self.assertTrue(
                        "total" in record, f"Unexpected non-record{record}."
                    )
                else:
                    location = record["record"]
                    if "merchant_location_key" in location:
                        if location["merchant_location_key"] == merchant_location_key:
                            confirmed = True
                            break
                    else:
                        self.fail(
                            f"A location is missing the merchant_location_key {record}."
                        )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        self.assertTrue(confirmed, "Failed to confirm that the new location exists.")

    def test_sell_create_or_replace_inventory_item(self):
        """
        See https://developer.ebay.com/api-docs/sell/inventory/static/overview.html &
        https://developer.ebay.com/api-docs/sell/inventory/resources/inventory_item/methods/createOrReplaceInventoryItem#h2-samples

        :return:
        """
        # Create a new inventory item.
        # A template for supplying all possible information about an inventory item.
        _body = {
            "availability": {
                "pickupAtLocationAvailability": [
                    {
                        "availabilityType": "AvailabilityTypeEnum : [IN_STOCK,OUT_OF_STOCK,SHIP_TO_STORE]",
                        "fulfillmentTime": {
                            "unit": "TimeDurationUnitEnum : [YEAR,MONTH,DAY,HOUR,CALENDAR_DAY,"
                            "BUSINESS_DAY,MINUTE,SECOND,MILLISECOND]",
                            "value": "integer",
                        },
                        "merchantLocationKey": "string",
                        "quantity": "integer",
                    }
                ],
                "shipToLocationAvailability": {
                    "availabilityDistributions": [
                        {
                            "fulfillmentTime": {
                                "unit": "TimeDurationUnitEnum : [YEAR,MONTH,DAY,HOUR,"
                                "CALENDAR_DAY,BUSINESS_DAY,MINUTE,SECOND,MILLISECOND]",
                                # noqa: E501
                                "value": "integer",
                            },
                            "merchantLocationKey": "string",
                            "quantity": "integer",
                        }
                    ],
                    "quantity": "integer",
                },
            },
            "condition": "ConditionEnum : [NEW,LIKE_NEW,NEW_OTHER,"
            "NEW_WITH_DEFECTS,MANUFACTURER_REFURBISHED,"
            "CERTIFIED_REFURBISHED,EXCELLENT_REFURBISHED,"
            "VERY_GOOD_REFURBISHED,GOOD_REFURBISHED,SELLER_REFURBISHED,"
            "USED_EXCELLENT,USED_VERY_GOOD,USED_GOOD,USED_ACCEPTABLE,FOR_PARTS_OR_NOT_WORKING]",
            # noqa: E501
            "conditionDescription": "string",
            "packageWeightAndSize": {
                "dimensions": {
                    "height": "number",
                    "length": "number",
                    "unit": "LengthUnitOfMeasureEnum : [INCH,FEET,CENTIMETER,METER]",
                    "width": "number",
                },
                "packageType": "PackageTypeEnum : [LETTER,BULKY_GOODS,CARAVAN,CARS,"
                "EUROPALLET,EXPANDABLE_TOUGH_BAGS,EXTRA_LARGE_PACK,"  # noqa: E501
                "FURNITURE,INDUSTRY_VEHICLES,LARGE_CANADA_POSTBOX,"
                "LARGE_CANADA_POST_BUBBLE_MAILER,LARGE_ENVELOPE,"
                "MAILING_BOX,MEDIUM_CANADA_POST_BOX,MEDIUM_CANADA_POST_BUBBLE_MAILER,"
                "MOTORBIKES,ONE_WAY_PALLET,PACKAGE_THICK_ENVELOPE,PADDED_BAGS,"
                "PARCEL_OR_PADDED_ENVELOPE,ROLL,SMALL_CANADA_POST_BOX,SMALL_CANADA_POST_BUBBLE_MAILER,"
                "TOUGH_BAGS,UPS_LETTER,USPS_FLAT_RATE_ENVELOPE,USPS_LARGE_PACK,VERY_LARGE_PACK,"
                "WINE_PAK]",
                "weight": {
                    "unit": "WeightUnitOfMeasureEnum : [POUND,KILOGRAM,OUNCE,GRAM]",
                    "value": "number",
                },
            },
            "product": {
                "aspects": "string",
                "brand": "string",
                "description": "string",
                "ean": ["string"],
                "epid": "string",
                "imageUrls": ["string"],
                "isbn": ["string"],
                "mpn": "string",
                "subtitle": "string",
                "title": "string",
                "upc": ["string"],
                "videoIds": ["string"],
            },
        }
        # A template for supplying limited information about an inventory item.
        body = {
            "availability": {"shipToLocationAvailability": {"quantity": 50}},
            "condition": "NEW",
            "product": {
                "title": "GoPro Hero4 Helmet Cam",
                "description": "New GoPro Hero4 Helmet Cam. Unopened box.",
                "imageUrls": [
                    "https://i.ebayimg.com/images/i/182196556219-0-1/s-l1000.jpg",
                    "https://i.ebayimg.com/images/i/182196556219-0-1/s-l1001.jpg",
                    "https://i.ebayimg.com/images/i/182196556219-0-1/s-l1002.jpg",
                ],
            },
        }

        # The natural language used in the body; see 'Local Support' in the following link for permitted values.
        # https://developer.ebay.com/api-docs/static/rest-request-components.html#HTTP
        content_language = "en-US"

        # The seller-defined SKU value for the inventory item, unique across the seller's inventory.
        length = random.randint(1, 50)
        allowed = (
            string.ascii_letters + string.digits + "_" + "-"
        )  # more might be allowed, eBay's docs are unclear
        sku = "".join(random.choice(allowed) for _i in range(length))

        try:
            self._api.sell_inventory_create_or_replace_inventory_item(
                body=body,
                content_language=content_language,
                content_type="application/json",
                sku=sku,
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")

    @unittest.skip  # TODO Finish the unit test and then attempt to relocate it to the APISandboxSingleSiteTests class.
    def test_file_upload(self):
        """
        Test uploading a file. Relevant eBay documentation:
        https://developer.ebay.com/api-docs/sell/feed/resources/task/methods/createTask
        https://developer.ebay.com/api-docs/sell/feed/resources/task/methods/uploadFile.
        """
        body = {
            "feedType": "LMS_ORDER_ACK",  # TODO Is this the correct feed type for use with sell_feed_upload_file?.
            "schemaVersion": "1.0",
        }
        try:
            self._api.sell_feed_create_task(body=body)
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            # TODO Somehow, get the task id from the sell_feed_create_task response header. Example from the header.
            # location:https://api.ebay.com/sell/feed/v1/task/task-11-1271150479
            # As of 2022-10-22, the Swagger code generated from eBay's OpenAPI contract doesn't support this.
            task_id = "task-11-1271150479"

            file_name = "test_file_upload.json"

            # TODO Somehow pass along the path and file name for the file to be uploaded.
            path_and_file_name = self._config_location = os.path.join(
                os.getcwd(), "test_file_upload.json"
            )
            # Lines like "local_var_files = {}" are found in src/ebay_rest/api/sell_feed/api/task_api.py
            # Instead of an empty dictionary, how do we make this happen?
            local_var_files = {"filename", path_and_file_name}
            # The Swagger code generated from eBay's OpenAPI contract doesn't support this. Checked on 2022-10-22.

            try:
                self._api.sell_feed_upload_file(task_id=task_id, file_name=file_name)
            except Error as error:
                self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")

    @unittest.skip  # TODO finish it
    def test_marketplace_account_deletion(self):
        """
        See https://developer.ebay.com/marketplace-account-deletion
        and https://developer.ebay.com/api-docs/commerce/notification/overview.html.

        # AsyncAPI specification
        # https://developer.ebay.com/cms/files/asyncapi/marketplace_account_deletion.yaml
        # https://www.asyncapi.com
        # https://github.com/dedoussis/asynction
        # https://github.com/dutradda/asyncapi-python

        :return:
        """
        # TODO get this from ebay_rest.json
        end_point = "https://e***********4.s*************.com/notification-endpoint"
        alert_email = "**@**.com"

        # The verification token has to be between 32 and 80 characters,
        # and allowed characters include alphanumeric characters, underscore (_),  and hyphen (-).
        # No other characters are allowed.
        # verification_token = "7*******-d***-***c-b***-***********a"
        length = random.randint(32, 80)
        allowed = string.ascii_letters + string.digits + "_" + "-"
        verification_token = "".join(random.choice(allowed) for _i in range(length))

        topic_id = "MARKETPLACE_ACCOUNT_DELETION"

        # confirm that the desired topic is available, eBay's recommended workflow does not require this
        try:
            result = self._api.commerce_notification_get_topics()
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            success = False
            key = "topics"
            if key in result:
                for topic in result[key]:
                    if topic["topic_id"] == topic_id:
                        if topic["status"] == "ENABLED":
                            success = True
                            break
            self.assertTrue(success)

        # ensure that an alert email is correctly configured
        try:
            result = self._api.commerce_notification_get_config()
        except Error as error:
            if error.reason != "Not Found":
                self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
            else:
                try:
                    config = {"alertEmail": alert_email}
                    self._api.commerce_notification_update_config(body=config)
                except Error as error:
                    self.fail(
                        f"Error {error.number} is {error.reason}  {error.detail}.\n"
                    )
        else:
            self.assertEqual(result["alert_email"], alert_email)

        # ensure that a destination is correctly configured
        # Note: The destination should be created and ready to respond with the expected
        # challengeResponse for the endpoint to be registered successfully.
        # Refer to the Notification API Overview for more information.
        # https://developer.ebay.com/api-docs/commerce/notification/overview.html
        try:
            result = self._api.commerce_notification_get_destinations()
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            if result["total"] == 0:
                try:
                    destination_request = {
                        "status": "ENABLED",
                        "deliveryConfig": {
                            "endpoint": end_point,
                            "verificationToken": verification_token,
                        },
                    }
                    self._api.commerce_notification_create_destination(
                        body=destination_request
                    )
                except Error as error:
                    self.fail(
                        f"Error {error.number} is {error.reason}  {error.detail}.\n"
                    )
                else:
                    pass  # TODO
            else:
                pass  # TODO

        # ensure subscribed
        # TODO

        # get notices
        # description: 'The Account Deletion payload.'
        #     username, string, The username for the user.
        #     userId, string, The immutable public userId for the user
        #     eiasToken, string, The legacy eiasToken specific to the user
        try:
            result = self._api.commerce_notification_get_topic(topic_id)
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            pass  # TODO
            self.assertTrue("Subscribe" not in result["description"])


class APISandboxDigitalSignatureTests(unittest.TestCase):
    """API tests that test eBay Digital Signatures and public/private key pairs"""

    @classmethod
    def setUpClass(cls):
        sandbox = True
        application = "sandbox_1" if sandbox else "production_1"
        user = "sandbox_1" if sandbox else "production_1"
        key_pair = "sandbox_1" if sandbox else "production_1"
        _api = API(
            application=application,
            user=user,
            header="US",
            key_pair=key_pair,
            digital_signatures=True,
        )
        original_private_key = _api._key_pair_token._private_key
        original_signing_key_id = _api._key_pair_token._signing_key_id
        if original_private_key and original_signing_key_id:
            cls.key_fail = None
        else:
            cls.key_fail = (
                "Need a private key and signing_key_id for Digital Signatures tests"
            )
        # retain only what the class methods need
        cls.application = application
        cls._api = _api
        cls.original_private_key = original_private_key
        cls.original_signing_key_id = original_signing_key_id
        cls.user = user
        cls.marketplace_id = _api._header["marketplace_id"]

    def setUp(self):
        # Reset private key
        self._api._key_pair_token._private_key = self.original_private_key
        if self.key_fail is not None:
            self.fail(self.key_fail)

    def test_001_get_signing_key(self):
        """Check that we can load all the remaining key information
        given the private key and signing_key_id.
        """
        key_pair = {
            "private_key": self.original_private_key,
            "signing_key_id": self.original_signing_key_id,
        }
        api = API(
            application=self.application,
            user=self.user,
            header="US",
            key_pair=key_pair,
            digital_signatures=True,
        )
        try:
            key = api.get_digital_signature_key(create_new=False)
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            self.assertEqual(key["private_key"], self.original_private_key)
            self.assertEqual(key["signing_key_id"], self.original_signing_key_id)

    def test_002_make_call_with_signature(self):
        """Check that we can make a call using the Digital Signature"""
        try:
            result = self._api.sell_finances_get_transaction_summary(
                filter="transactionStatus:{PAYOUT}",
                x_ebay_c_marketplace_id=self.marketplace_id,
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            self.assertTrue("credit_count" in result)
            # Break the private key and try again
            # This is an example key from draft-ietf-httpbis-message-signatures-15
            self._api._key_pair_token._private_key = (
                "MC4CAQAwBQYDK2VwBCIEIJ+DYvh6SEqVTm50DFtMDoQikTmiCqirVv9mWG9qfSnF"
            )
            try:
                self._api.sell_finances_get_transaction_summary(
                    filter="transactionStatus:{PAYOUT}",
                    x_ebay_c_marketplace_id=self.marketplace_id,
                )
            except Error as error:
                self.assertEqual(error.number, 99403)
                # Check for eBay 'Signature validation failed' error
                ebay_error = loads(error.detail)
                signature_validation_failed = (215120, 215121, 215122)
                self.assertTrue(
                    ebay_error["errors"][0]["errorId"] in signature_validation_failed
                )
            else:
                self.fail("Did not fail with invalid private key!")

    # This test permanently creates a new public/private key pair which cannot
    # be removed, hence it is skipped by default.
    @unittest.skip
    def test_003_create_signing_key(self):
        """Check that we can create a new public/private key."""
        self._api._key_pair_token._private_key = None
        self._api._key_pair_token._signing_key_id = None
        with self.assertRaises(Error):
            _key = self._api.get_digital_signature_key(create_new=False)
        key = self._api.get_digital_signature_key(create_new=True)
        self.assertTrue(key["private_key"])
        self.assertNotEqual(key["private_key"], self.original_private_key)
        try:
            result = self._api.sell_finances_get_transaction_summary(
                filter="transactionStatus:{PAYOUT}",
                x_ebay_c_marketplace_id=self.marketplace_id,
            )
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            self.assertTrue("credit_count" in result)


class DateTimeTests(unittest.TestCase):
    def test_date_time_now(self):
        self.assertTrue(
            isinstance(DateTime.now(), datetime.date),
            msg="Unexpected return type from a DateTime member function.",
        )

    def test_date_time_from_string(self):
        self.assertTrue(
            isinstance(DateTime.from_string("2004-08-04T19:09:02.768Z"), datetime.date),
            msg="Unexpected return type from a DateTime member function.",
        )

    def test_date_time_to_string(self):
        self.assertTrue(
            isinstance(DateTime.to_string(DateTime.now()), str),
            msg="Unexpected return type from a DateTime member function.",
        )


class TokenTests(unittest.TestCase):
    def test_get_authorization_code(self):
        """
        Notes:
        1. A web browser window should pop up while this test successfully runs.
        2. eBay also refers to the authorization code as a token refresh token.
        """
        try:
            # The user sand_box_2 should be a copy of sand_box_1 without refresh token values.
            api = API(application="sandbox_1", user="sandbox_2", header="US")
        except Error as error:
            self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
        else:
            # Try a method that needs a user refresh token.
            try:
                result = api.sell_compliance_get_listing_violations_summary(
                    x_ebay_c_marketplace_id=api._header["marketplace_id"]
                )
            except Error as error:
                self.fail(f"Error {error.number} is {error.reason}  {error.detail}.\n")
            else:
                # Do something that makes use of the result to avoid an IDE warning about not using the variable.
                self.assertIsNotNone("violation_summaries" in result)


class MultitonTests(unittest.TestCase):
    def test_help(self):
        """Documentation from the wrapped class should be returned instead of Multiton."""
        doc_string = API.__doc__
        self.assertTrue(
            "Multiton" not in doc_string and "API" in doc_string,
            msg="Double-check functools.update_wrapper in multiton.py.",
        )


class ReferenceTests(unittest.TestCase):
    def test_get_application_scopes(self):
        self.assertIsNotNone(
            Reference.get_application_scopes(), msg="Failed to load application scopes."
        )

    def test_get_country_codes(self):
        self.assertIsNotNone(
            Reference.get_country_codes(), msg="Failed to load country codes."
        )

    def test_get_currency_codes(self):
        self.assertIsNotNone(
            Reference.get_currency_codes(), msg="Failed to load currency codes."
        )

    def test_global_id_values(self):
        self.assertIsNotNone(
            Reference.get_global_id_values(), msg="Failed to load global id values."
        )

    def test_marketplace_id_values(self):
        self.assertIsNotNone(
            Reference.get_marketplace_id_values(),
            msg="Failed to load marketplace id values.",
        )

    def test_get_user_scopes(self):
        self.assertIsNotNone(
            Reference.get_user_scopes(), msg="Failed to load user scopes."
        )


if __name__ == "__main__":
    unittest.main()
