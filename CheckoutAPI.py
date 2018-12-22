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

    def validate_parameters(self, name, price_per_unit, unit_type):
        if not type(name) == str: raise(ValueError)
        if not (type(price_per_unit) == int or type(price_per_unit) == float): raise(ValueError)
        if not unit_type in valid_unit_types: raise(ValueError)

    def get_price(self):
        return self.price_per_unit

    def update_price(self, new_price):
        self.validate_parameters(self.name, new_price, self.unit_type)
        self.price_per_unit = new_price

    def markdown_price(self, markdown):
        if markdown is None or markdown < 0: raise(ValueError)
        self.update_price(self.price_per_unit - markdown)

    def set_special_price(self):
        return


class Checkout():
    def __init__():
        return

    def add_item_to_store():
        return

    def get_items_in_cart():
        return

    def add_item_to_cart():
        return

    def remove_item_from_cart():
        return


class CheckoutAPI(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        return

    def do_POST(self):
        return

    def do_PUT(self):
        return

    def do_DELETE(self):
        return
