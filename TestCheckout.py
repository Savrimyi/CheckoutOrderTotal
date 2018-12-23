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

    def test_add_many_items_to_cart(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.assertEquals([{"item":self.test_item, "quantity": 12}], self.test_checkout.get_items_in_cart())

    def test_add_negative_items_to_cart(self):
        with self.assertRaises(Exception):
            self.test_checkout.add_item_to_cart("potatoes", -4)

    def test_add_item_to_cart_doesnt_exist(self):
        with self.assertRaises(Exception):
            self.test_checkout.add_item_to_cart("oranges", 1)

    def test_add_item_to_store_with_negative_price(self):
        with self.assertRaises(Exception):
            self.test_checkout.add_item_to_store("oranges", -1, "each")

    def test_remove_negative_items_from_cart(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        with self.assertRaises(Exception):
            self.test_checkout.remove_item_from_cart("potatoes", -3)

    def test_get_checkout_total(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.assertEquals(self.test_checkout.get_checkout_total(), 20)

    def test_get_checkout_total_with_special(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.test_checkout.get_item_information("potatoes").set_special_price("3 for $10")
        self.assertEquals(self.test_checkout.get_checkout_total(), 15)

    def test_get_checkout_total_invalidated_special(self):
        self.test_checkout.add_item_to_cart("potatoes", 4)
        self.test_checkout.get_item_information("potatoes").set_special_price("3 for $10")
        self.assertEquals(self.test_checkout.get_checkout_total(), 15)
        self.test_checkout.remove_item_from_cart("potatoes", 3)
        self.assertEquals(self.test_checkout.get_checkout_total(), 5)

    def test_get_checkout_total_with_percent_off_special(self):
        self.test_checkout.add_item_to_cart("potatoes", 40)
        self.test_checkout.get_item_information("potatoes").set_special_price("buy 10 items, get 3 at %56 off")
        self.assertEquals(self.test_checkout.get_checkout_total(), 180.2)

    def test_get_checkout_total_with_special_and_limit(self):
        self.test_checkout.add_item_to_cart("potatoes", 40)
        self.test_checkout.get_item_information("potatoes").set_special_price("buy 10 items, get 3 at %56 off. limit 26.")
        self.assertEquals(self.test_checkout.get_checkout_total(), 100+16.8+70)

    def test_get_checkout_total_invalidated_special_and_limit(self):
        self.test_checkout.add_item_to_cart("potatoes", 40)
        self.test_checkout.get_item_information("potatoes").set_special_price("buy 10 items, get 3 at %56 off. limit 26.")
        self.assertEquals(self.test_checkout.get_checkout_total(), 100+16.8+70)
        self.test_checkout.remove_item_from_cart("potatoes", 37)
        self.assertEquals(self.test_checkout.get_checkout_total(), 15)
