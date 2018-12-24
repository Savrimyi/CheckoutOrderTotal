import unittest
import requests
import json

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url = "http://localhost/"
OK = 200
CREATED = 201
NOT_FOUND = 404
COMPLETED_NO_CONTENT = 204

class CheckoutAPITestCase(unittest.TestCase):

    def test_add_item_to_store_POST(self):
        self.fail("Not implemented")

    def test_add_item_without_data_POST(self):
        self.fail("Not implemented")

    def test_add_item_invalid_request_type(self):
        self.fail("Not implemented")

    def test_set_special_price_POST(self):
        self.fail("Not implemented")

    def test_set_special_price_without_data_POST(self):
        self.fail("Not implemented")

    def test_set_special_price_invalid_request_type(self):
        self.fail("Not implemented")

    def test_markdown_price_POST(self):
        self.fail("Not implemented")

    def test_markdown_without_data_POST(self):
        self.fail("Not implemented")

    def test_markdown_invalid_request_type(self):
        self.fail("Not implemented")

    def test_get_item_info_GET(self):
        self.fail("Not implemented")

    def test_get_item_invalid_request_type(self):
        self.fail("Not implemented")

    def test_remove_item_from_store_DELETE(self):
        self.fail("Not implemented")

    def test_remove_item_not_in_store_DELETE(self):
        self.fail("Not implemented")

    def test_remove_item_invalid_request_type(self):
        self.fail("Not implemented")

    def test_get_items_in_store_GET(self):
        self.fail("Not implemented")

    def test_get_items_in_store_invalid_request_type(self):
        self.fail("Not implemented")

    def test_add_item_to_cart_POST(self):
        self.fail("Not implemented")

    def test_add_items_to_cart_invalid_data_POST(self):
        self.fail("Not implemented")

    def test_add_items_to_cart_invalid_request_type(self):
        self.fail("Not implemented")

    def test_get_items_in_cart_GET(self):
        self.fail("Not implemented")

    def test_get_items_in_cart_invalid_request_type(self):
        self.fail("Not implemented")

    def test_get_item_info_from_cart_GET(self):
        self.fail("Not implemented")

    def test_get_item_info_from_cart_doesnt_exist(self):
        self.fail("Not implemented")

    def test_get_items_from_cart_invalid_request_type(self):
        self.fail("Not implemented")

    def test_remove_item_from_cart_DELETE(self):
        self.fail("Not implemented")

    def test_remove_item_from_cart_doesnt_exist(self):
        self.fail("Not implemented")

    def test_remove_item_from_cart_invalid_request_type(self):
        self.fail("Not implemented")

    def test_get_checkout_total(self):
        self.fail("Not implemented")
