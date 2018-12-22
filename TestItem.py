import unittest
from CheckoutAPI import Item


class CheckoutAPIItemTestCase(unittest.TestCase):

    test_item = Item("potatoes", 5, "each")

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

    def test_get_price_basic(self):
        self.assertEquals(self.test_item.get_price(), 5)

    def test_update_price(self):
        self.test_item.update_price(6)
        self.assertEquals(self.test_item.get_price(), 6)

    def test_update_price_invalid_input_string(self):
        with self.assertRaises(Exception):
            self.test_item.update_price("Bad price")

    def test_markdown_price(self):
        start_price = self.test_item.get_price()
        markdown = 4
        self.test_item.markdown_price(markdown)
        end_price = self.test_item.get_price()
        self.assertEquals(end_price, (start_price - markdown))

    def test_markdown_price_invalid_input_string(self):
        with self.assertRaises(Exception):
            self.test_item.markdown_price("not a real price")

    def test_markdown_price_null_input(self):
        with self.assertRaises(Exception):
            self.test_item.markdown_price(None)

    def test_markdown_price_negative_input(self):
        with self.assertRaises(Exception):
            self.test_item.markdown_price(-234)

    def test_set_special_price(self):
        self.fail("Test not implemented")
