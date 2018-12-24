import socketserver
import http.server
import re
import json

valid_unit_types = ['each', 'per pound']

class Item():
    def __init__(self, name, price_per_unit, unit_type):
        #Validate input before initializing
        self.validate_parameters(name, price_per_unit, unit_type)
        self.name = name
        self.price_per_unit = price_per_unit
        self.unit_type = unit_type
        self.special_price = None
        self.markdown = 0

    def validate_parameters(self, name, price_per_unit, unit_type):
        if not type(name) == str: raise(ValueError)
        if not (type(price_per_unit) == int or type(price_per_unit) == float) or price_per_unit < 0: raise(ValueError)
        if not unit_type in valid_unit_types: raise(ValueError)

    def get_price(self):
        return self.price_per_unit - self.markdown

    def update_price(self, new_price):
        self.validate_parameters(self.name, new_price, self.unit_type)
        self.price_per_unit = new_price
        self.markdown = 0

    def markdown_price(self, markdown):
        if markdown is None or markdown < 0: raise(ValueError)
        self.markdown = markdown

    def get_special_price(self):
        return self.special_price

    def set_special_price(self, special):

        if special is None or \
        re.search(r'^buy \d+ items, get \d+ at %\d+ off', special.lower()) or \
        re.search(r'^buy \d+ get \d+ (free|half off)', special.lower()) or \
        re.search(r'^\d+ for \$\d+', special.lower()) or \
        re.search(r'^buy \d+, get \d+ of equal or lesser value for %\d+ off', special.lower()):
            if re.search(r'%\d+ off', special.lower()):
                percentage = re.search(r'%\d+ off', special.lower()).group().strip('%').strip(' off')
                if int(percentage) > 100 or int(percentage) < 0:
                    raise(ValueError)
            self.special_price = special
        else:
            raise(ValueError)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.name == other.name and \
                self.price_per_unit == other.price_per_unit and \
                self.unit_type == other.unit_type and \
                self.special_price == other.special_price

class Checkout():
    def __init__(self):
        self.store = []
        self.cart = []

    def add_item_to_store(self, name, price_per_unit, unit_type):
        for item in self.store:
            if item.name == name:
                #Item is already in store
                raise(ValueError)
        self.store.append(Item(name, price_per_unit, unit_type))

    def get_item_information(self, name):
        matches = list(filter(lambda x: x.name == name, self.store))
        if matches == []:
            return None
        else:
            return matches[0]

    def get_items_in_store(self):
        return self.store

    def get_items_in_cart(self):
        return self.cart

    def add_item_to_cart(self, name, quantity):
        item = self.get_item_information(name)
        if item is None or quantity < 0: raise(ValueError)
        item_in_cart = self.get_item_information_from_cart(name)
        if item_in_cart is not None:
            item_in_cart['quantity'] += quantity
        else:
            self.cart.append({"item": item, "quantity": quantity})

    def get_item_information_from_cart(self, name):
        matches = list(filter(lambda x: x['item'].name == name, self.cart))
        if matches == []:
            return None
        else:
            return matches[0]

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

    def get_checkout_total(self):
        total = 0.0
        for item in self.cart:
            special = item['item'].get_special_price()
            if special is not None:
                special = special.lower()
                if "free" in special or "half off" in special:
                    special = special.replace("free","at %100 off").replace("half off","at %50 off").replace("get", "items, get")

                if "of equal or lesser value for" in special:
                    special = special.replace("of equal or lesser value for","at").replace(","," items,")

                if re.search(r'^buy \d+ items, get \d+ at %\d+ off', special):
                    pattern = re.compile(r'^buy (?P<purchase_requirement>\d+) items, get (?P<discounted_quantity>\d+) at %(?P<percentage_discount>\d+) off')
                    match = pattern.match(special).groupdict()
                    minimum_items = int(match['purchase_requirement']) + int(match['discounted_quantity'])
                    percentage_discount = int(match['percentage_discount']) / 100.0
                    if re.search(r'^buy \d+ items, get \d+ at %\d+ off. limit (\d+)', special):
                        pattern_with_limit = re.compile(r'^buy \d+ items, get \d+ at %\d+ off. limit (?P<limit>\d+)')
                        match_with_limit = pattern_with_limit.match(special).groupdict()
                        max_discount_sets = int(match_with_limit['limit']) / minimum_items
                        max_discounted_items = max_discount_sets * int(match['discounted_quantity'])
                        discounted_items = int(int(item['quantity']) / minimum_items) * int(match['discounted_quantity'])
                        if discounted_items > max_discounted_items:
                            discounted_items = max_discounted_items
                    else:
                        discounted_items = int(int(item['quantity']) / minimum_items) * int(match['discounted_quantity'])
                    full_price_items = int(item['quantity']) - discounted_items
                    total += (item['item'].get_price() * full_price_items) + (item['item'].get_price() * (1 - percentage_discount) * discounted_items)

                elif re.search(r'^\d+ for \$\d+', special):
                    pattern = re.compile(r'^(?P<quantity>\d+) for \$(?P<price>\d+)')
                    match = pattern.match(special).groupdict()
                    if item['quantity'] > int(match['quantity']):
                        discount_count = int(item['quantity'] / int(match['quantity']))
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

                # elif re.search(r'^buy \d+ items, get \d+ of equal or lesser value for %\d+ off', special):
                #     pattern = re.compile(r'^buy (?P<purchase_requirement>\d+) items, get (?P<discounted_quantity>\d+) of equal or lesser value for %(?P<percentage_discount>\d+) off')
                #     match = pattern.match(special).groupdict()
                #     print("Special: ", match)
            else:
                total += item['item'].get_price() * item['quantity']
        return total

class CheckoutAPI(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        return

    def do_POST(self):
        return

    def do_PUT(self):
        return

    def do_DELETE(self):
        return
