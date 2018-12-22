import unittest
from CheckoutAPI import Item


class CheckoutAPIItemTestCase(unittest.TestCase):

    def test_init_item_with_info(self):
        try:
            item = Item("potatoes", 5, "each")
            item = Item("potatoes", 2.45, "per pound")
        except Exception as e:
            self.fail("Raised Unexpected Exception: " + str(e))

    def test_init_with_integer_for_name(self):
        with self.assertRaises(Exception):
            item = Item(56, 5, "each")

    def test_init_with_string_for_price(self):
        with self.assertRaises(Exception):
            item = Item("potatoes", "five", "each")

    def test_init_with_invalid_per_unit_type(self):
        with self.assertRaises(Exception):
            item = Item("potatoes", 5, "invalid string")

    def test_get_price(self):
        self.fail("Test not implemented")

    def test_update_price(self):
        self.fail("Test not implemented")

    def test_markdown_price(self):
        self.fail("Test not implemented")

    def test_set_special_price(self):
        self.fail("Test not implemented")
