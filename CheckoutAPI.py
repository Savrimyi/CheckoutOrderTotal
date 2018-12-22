import socketserver
import http.server
import re
import json

valid_unit_types = ['each', 'per pound']

class Item():
    def __init__(self, name, price_per_unit, unit_type):
        #Validate input before initializing
        if not type(name) == str: raise(ValueError)
        if not (type(price_per_unit) == int or type(price_per_unit) == float): raise(ValueError)
        if not unit_type in valid_unit_types: raise(ValueError)
        self.name = name
        self.price_per_unit = price_per_unit
        self.unit_type = unit_type

    def get_price():
        return

    def update_price():
        return

    def markdown_price():
        return

    def set_special_price():
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
