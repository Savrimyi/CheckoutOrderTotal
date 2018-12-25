import unittest
from PointOfSale import PointOfSale
import json

class PointOfSaleTestCase(unittest.TestCase):
    """
        Test cases for the Cashier's Point of Sale system
    """

    def setUp(self):
        self.test_point_of_sale = PointOfSale()
        self.test_point_of_sale.call_api_post_add_item_to_store("carrots", 2, "each")


    ### POST request (Information changing) tests

    def test_valid_input_add_item_to_store(self):
        self.test_point_of_sale.call_api_delete_from_store("carrots")
        item  = self.test_point_of_sale.call_api_post_add_item_to_store("carrots", 2, "each")
        self.assertEquals(item['name'], "carrots")

    def test_valid_input_set_special_price(self):
        item  = self.test_point_of_sale.call_api_post_set_special_price("carrots", "3 for $5")
        self.assertEquals(item['special_price'], "3 for $5")

    def test_valid_input_markdown_price(self):
        item  = self.test_point_of_sale.call_api_post_markdown_price("carrots", 1)
        self.assertEquals(item['markdown'], 1)

    def test_valid_input_add_item_to_cart(self):
        item  = self.test_point_of_sale.call_api_post_add_item_to_cart("carrots", 3)
        self.assertEquals(item['quantity'], 3)

    ### GET request (information retreival) tests

    def test_valid_input_get_item_from_store(self):
        item  = self.test_point_of_sale.call_api_get_item_info("carrots")
        self.assertEquals(item['name'], "carrots")

    def test_valid_input_get_items_in_store(self):
        items_in_store  = self.test_point_of_sale.call_api_get_items_in_store()
        item_names = [json.loads(item)['name'] for item in items_in_store]
        self.assertTrue("carrots" in item_names)

    def test_valid_input_get_items_in_cart(self):
        items_in_cart  = self.test_point_of_sale.call_api_get_items_in_cart()
        item_names = [json.loads(item['item'])['name'] for item in items_in_cart]
        self.assertTrue("carrots" in item_names)

    def test_valid_input_get_item_info_cart(self):
        item  = self.test_point_of_sale.call_api_get_item_info_cart("carrots")
        self.assertEquals(item['item']['name'], "carrots")

    def test_valid_input_get_checkout_total(self):
        total  = self.test_point_of_sale.call_api_get_checkout_total()
        self.assertTrue(total >  5)

    ### DELETE request (Information removal) tests

    def test_valid_input_delete_from_store(self):
        deleted_item_response = self.test_point_of_sale.call_api_delete_from_store("carrots")
        self.assertTrue(deleted_item_response)

    def test_valid_input_delete_from_cart(self):
        deleted_item_response = self.test_point_of_sale.call_api_delete_from_cart("carrots", 1)
        self.assertTrue(deleted_item_response)
