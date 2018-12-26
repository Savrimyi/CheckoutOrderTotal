import re
import json

from Item import Item

class Checkout():
    """
        This object runs the store.
        It creates and stores Items in the store and maintains a cart for customers to track their purchases.
    """
    def __init__(self):
        self.store = []
        self.cart = []

    """ If an Item is not already in the store, this will add it to the store. """
    def add_item_to_store(self, name, price_per_unit, unit_type):
        for item in self.store:
            if item.name == name:
                #Item is already in store
                raise(ValueError)
        self.store.append(Item(name, price_per_unit, unit_type))

    """ Retreives Item information for an Item in the store """
    def get_item_information(self, name):
        matches = list(filter(lambda x: x.name == name, self.store))
        if matches == []:
            return None
        else:
            return matches[0]

    """ Returns the list of Items in the store available for sale. """
    def get_items_in_store(self):
        return self.store

    """ Returns the list of Items in the customer's cart to be purchased. """
    def get_items_in_cart(self):
        return self.cart

    """ Scan an Item to indicate that the customer is purchasing it. """
    def add_item_to_cart(self, name, quantity):
        item = self.get_item_information(name)
        if item is None or quantity < 0: raise(ValueError)      #Throw an error if they scan something the store does not sell.
        item_in_cart = self.get_item_information_from_cart(name)
        if item_in_cart is not None:
            item_in_cart['quantity'] += quantity        #If they have the same Item in their cart, increase the quantity.
        else:
            self.cart.append({"item": item, "quantity": quantity})      #If this is a new Item, add it to their cart.

    """ Get information about an Item in the cart. """
    def get_item_information_from_cart(self, name):
        matches = list(filter(lambda x: x['item'].name == name, self.cart))
        if matches == []:
            return None
        else:
            return matches[0]

    """ Remove an Item or quantity of Items from the cart. """
    def remove_item_from_cart(self, name, quantity):
        item_in_cart = self.get_item_information_from_cart(name)
        if item_in_cart is None or quantity < 1:
            raise(ValueError)
        elif item_in_cart['quantity'] > quantity:
            item_in_cart['quantity'] -= quantity
        elif item_in_cart['quantity'] == quantity:
            self.cart.remove(item_in_cart)
        else:
            raise(ValueError)

    """ Remove an item from the store. """
    def remove_item_from_store(self, name):
        item_in_store = self.get_item_information(name)
        if item_in_store is None: raise(ValueError)
        self.store.remove(item_in_store)

    """ Calculates the checkout total using Item information, including specials and markdowns. """
    def get_checkout_total(self):
        total = 0.0
        for item in self.cart:
            special = item['item'].get_special_price()
            if special is not None:
                special = special.lower()

                #Translate a "free" or "half off" discount into a percentage discount to deduplicate code.
                if "free" in special or "half off" in special:
                    special = special.replace("free","at %100 off").replace("half off","at %50 off").replace("get", "items, get")

                #I was not sure if this function is required if all Items of one type share a price and markdown conditions. I may refactor this later.
                if "of equal or lesser value for" in special:
                    special = special.replace("of equal or lesser value for","at").replace(","," items,")

                #Determine which special discount to apply.

                #Percentage discount special
                if re.search(r'^buy \d+ items, get \d+ at %\d+ off', special):
                    pattern = re.compile(r'^buy (?P<purchase_requirement>\d+) items, get (?P<discounted_quantity>\d+) at %(?P<percentage_discount>\d+) off')
                    match = pattern.match(special).groupdict()
                    minimum_items = int(match['purchase_requirement']) + int(match['discounted_quantity'])
                    percentage_discount = int(match['percentage_discount']) / 100.0

                    #If there is a limit on the discount, only apply discount up to max.
                    if re.search(r'^buy \d+ items, get \d+ at %\d+ off. limit (\d+)', special):
                        pattern_with_limit = re.compile(r'^buy \d+ items, get \d+ at %\d+ off. limit (?P<limit>\d+)')
                        match_with_limit = pattern_with_limit.match(special).groupdict()
                        max_discount_sets = int(match_with_limit['limit']) / minimum_items
                        max_discounted_items = max_discount_sets * int(match['discounted_quantity'])
                        discounted_items = int(int(item['quantity']) / minimum_items) * int(match['discounted_quantity'])
                        if discounted_items > max_discounted_items:
                            discounted_items = max_discounted_items

                    #Else, apply discount to all available Items of this type.
                    else:
                        discounted_items = int(int(item['quantity']) / minimum_items) * int(match['discounted_quantity'])
                    full_price_items = int(item['quantity']) - discounted_items
                    total += (item['item'].get_price() * full_price_items) + (item['item'].get_price() * (1 - percentage_discount) * discounted_items)

                # N for $N special
                elif re.search(r'^\d+ for \$\d+', special):
                    pattern = re.compile(r'^(?P<quantity>\d+) for \$(?P<price>\d+)')
                    match = pattern.match(special).groupdict()
                    if item['quantity'] > int(match['quantity']):
                        discount_count = int(item['quantity'] / int(match['quantity']))

                        #Same as previous block, check for limit condition.
                        if re.search(r'^^\d+ for \$\d+. limit (\d+)', special):
                            pattern_with_limit = re.compile(r'^\d+ for \$\d+. limit (?P<limit>\d+)')
                            match_with_limit = pattern_with_limit.match(special).groupdict()
                            max_discount_sets = int(match_with_limit['limit']) / int(match['quantity'])
                            if max_discount_sets < discount_count:
                                discount_count = max_discount_sets
                        remainder = item['quantity'] - (discount_count * int(match['quantity']))
                        total += discount_count * float(match['price']) + item['item'].get_price() * remainder
                    else:
                        total += item['item'].get_price() * item['quantity']

                #     Code left behind from deduplication, but left in comment in case I refactor the "equal or less than " conditions
                #     elif re.search(r'^buy \d+ items, get \d+ of equal or lesser value for %\d+ off', special):
                #     pattern = re.compile(r'^buy (?P<purchase_requirement>\d+) items, get (?P<discounted_quantity>\d+) of equal or lesser value for %(?P<percentage_discount>\d+) off')
                #     match = pattern.match(special).groupdict()
                #     print("Special: ", match)

            #There is no discount applied.
            else:
                total += item['item'].get_price() * item['quantity']
        return total

    """ Returns the Item in the form of a dictionary """
    def dict(self):
        checkout_dict = {}
        checkout_dict['items_in_store'] = self.store
        checkout_dict['items_in_cart'] = self.cart
        return checkout_dict

    """ Returns the Item as JSON, to be used by API """
    def json(self):
        checkout_dict = {}
        checkout_dict['items_in_store'] = [x.json() for x in self.store]
        checkout_dict['items_in_cart'] = [{"item": x['item'].json(), "quantity": x['quantity']} for x in self.cart]
        return json.dumps(checkout_dict)

    """ Get the list of items in the store as JSON. """
    def get_store_as_json(self):
        return json.dumps({"items_in_store": [x.json() for x in self.store]})

    """ Get the list of items in the customer's cart as JSON. """
    def get_cart_as_json(self):
        return json.dumps({"items_in_cart": [{"item": x['item'].json(), "quantity": x['quantity']} for x in self.cart]})
