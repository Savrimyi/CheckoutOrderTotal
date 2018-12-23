import unittest
from CheckoutAPI import Checkout
from CheckoutAPI import Item

class CheckoutAPICheckoutTestCase(unittest.TestCase):


    def setUp(self):
        self.test_checkout = Checkout()
        self.test_item = Item("potatoes", 5, "each")
        self.test_checkout.add_item_to_store("potatoes", 5, "each")

    def test_init_checkout(self):
        checkout = Checkout()
        self.assertTrue(checkout)

    def test_add_item_to_store(self):
        self.test_checkout.add_item_to_store("bread", 5, "each")
        self.assertEquals(Item("bread", 5, "each"), self.test_checkout.get_item_information("bread"))

    def test_get_items_in_store(self):
        expected_items_in_store = [self.test_item]
        items_in_store = self.test_checkout.get_items_in_store()
        self.assertEquals(items_in_store, expected_items_in_store)

    def test_add_item_to_cart(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.assertTrue({"item":self.test_item, "quantity": 4} in self.test_checkout.get_items_in_cart())

    def test_get_items_in_cart(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.assertEquals([{"item":self.test_item, "quantity": 4}], self.test_checkout.get_items_in_cart())

    def test_remove_item_from_cart(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.test_checkout.remove_item_from_cart("potatoes", 3)
        self.assertEquals([{"item":self.test_item, "quantity": 1}], self.test_checkout.get_items_in_cart())
        self.test_checkout.remove_item_from_cart("potatoes", 1)
        self.assertEquals([], self.test_checkout.get_items_in_cart())
