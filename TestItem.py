import unittest
from Item import Item


class ItemTestCase(unittest.TestCase):
    """
        Test cases for the Item object.
    """

    #This runs before tests; used to set up.
    def setUp(self):
        self.test_item = Item("potatoes", 5, "each")

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

    def test_set_and_get_special_price_percent_off(self):
        self.test_item.set_special_price("buy 10 items, get 3 at %56 off")
        self.assertEquals("buy 10 items, get 3 at %56 off", self.test_item.get_special_price())

    def test_set_special_price_N_for_N(self):
        self.test_item.set_special_price("5 for $10")
        self.assertEquals("5 for $10", self.test_item.get_special_price())

    def test_set_special_price_with_limit(self):
        self.test_item.set_special_price("5 for $10. limit 6.")
        self.assertEquals("5 for $10. limit 6.", self.test_item.get_special_price())

    def test_set_special_price_free_item(self):
        self.test_item.set_special_price("buy 4 get 5 free")
        self.assertEquals("buy 4 get 5 free", self.test_item.get_special_price())

    def test_set_special_price_half_off_item(self):
        self.test_item.set_special_price("buy 4 get 5 half off")
        self.assertEquals("buy 4 get 5 half off", self.test_item.get_special_price())

    def test_set_special_price_equal_or_lesser_value(self):
        #Buy N, get M of equal or lesser value for %X off
        self.test_item.set_special_price("buy 4, get 5 of equal or lesser value for %10 off")
        self.assertEquals("buy 4, get 5 of equal or lesser value for %10 off", self.test_item.get_special_price())

    def test_set_special_price_invalid_input(self):
        with self.assertRaises(Exception):
            self.test_item.set_special_price("this probably wont match any regex")

    def test_set_special_price_invalid_number_of_items(self):
        with self.assertRaises(Exception):
            self.test_item.set_special_price("buy -4, get 5 of equal or lesser value for %10 off")
        with self.assertRaises(Exception):
            self.test_item.set_special_price("buy 4, get -5 of equal or lesser value for %10 off")
        with self.assertRaises(Exception):
            self.test_item.set_special_price("-5 for $10")
        with self.assertRaises(Exception):
            self.test_item.set_special_price("buy 4 get -5 free")
        with self.assertRaises(Exception):
            self.test_item.set_special_price("buy -4 get 5 free")

    def test_set_special_price_invalid__percentage_off(self):
        with self.assertRaises(Exception):
            self.test_item.set_special_price("buy 4, get 5 of equal or lesser value for %-10 off")
        with self.assertRaises(Exception):
            self.test_item.set_special_price("buy 4, get 5 of equal or lesser value for %300 off")

    def test_equals(self):
        test_item_1 = Item("potatoes", 5, "each")
        test_item_2 = Item("potatoes", 5, "each")
        self.assertEquals(test_item_1, test_item_2)

    def test_not_equals(self):
        test_item_1 = Item("potatoes", 5, "each")
        self.assertNotEquals(test_item_1, "string")
        self.assertNotEquals(test_item_1, 1234)
        self.assertNotEquals(test_item_1, None)
