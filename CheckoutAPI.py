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

    def validate_parameters(self, name, price_per_unit, unit_type):
        if not type(name) == str: raise(ValueError)
        if not (type(price_per_unit) == int or type(price_per_unit) == float) or price_per_unit < 0: raise(ValueError)
        if not unit_type in valid_unit_types: raise(ValueError)

    def get_price(self):
        return self.price_per_unit

    def update_price(self, new_price):
        self.validate_parameters(self.name, new_price, self.unit_type)
        self.price_per_unit = new_price

    def markdown_price(self, markdown):
        if markdown is None or markdown < 0: raise(ValueError)
        self.update_price(self.price_per_unit - markdown)

    def get_special_price(self):
        return self.special_price

    def set_special_price(self, special):

        if special is None or \
        re.search(r'^buy \d+ items, get \d+ at %\d+ off', special.lower()) or \
        re.search(r'^buy \d+ items, get \d+ (free|half off)', special.lower()) or \
        re.search(r'^\d+ for \$\d+', special.lower()) or \
        re.search(r'^buy \d+ items, get \d+ of equal or lesser value for %\d+ off', special.lower()):
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
        print("matches: ", matches)
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
                #do special stuff
                if re.search(r'^buy \d+ items, get \d+ at %\d+ off', special.lower()):
                    return
                elif re.search(r'^buy \d+ items, get \d+ (free|half off)', special.lower()):
                    return
                elif re.search(r'^\d+ for \$\d+', special.lower()):
                    return
                elif re.search(r'^buy \d+ items, get \d+ of equal or lesser value for %\d+ off', special.lower()):
                    return
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
