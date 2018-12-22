import unittest
from CheckoutAPI import Item


class CheckoutAPIItemTestCase(unittest.TestCase):

    def test_init_item_with_info(self):
        try:
            item = Item("potatoes", 5, "each")
        except Exception as e:
            self.fail("Raised Unexpected Exception: " + str(e))

    def test_get_price(self):
        self.fail("Test not implemented")

    def test_update_price(self):
        self.fail("Test not implemented")

    def test_markdown_price(self):
        self.fail("Test not implemented")

    def test_set_special_price(self):
        self.fail("Test not implemented")
