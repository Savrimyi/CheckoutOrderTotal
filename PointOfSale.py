import re
import requests
import json

headers = {'Content-type': 'application/json'}
url = "http://localhost:8080/"
OK = 200
CREATED = 201
NOT_FOUND = 404
COMPLETED_NO_CONTENT = 204

class PointOfSale():
    """
        This Point of Sale object will take user input and translate it into API calls.
    """
    def __init__(self):
        return

    def call_api_get_item_info(self, item_name):
        item = requests.get(url+'api/get_item_info/'+item_name, json={"key": "value"}, headers=headers)
        return item.json()

    def call_api_get_items_in_store(self):
        items_in_store = requests.get(url+'api/get_items_in_store/', json={"key": "value"})
        return items_in_store.json()['items_in_store']

    def call_api_get_items_in_cart(self):
        items_in_cart = requests.get(url+'api/get_items_in_cart/', json={"key": "value"})
        return items_in_cart.json()['items_in_cart']

    def call_api_get_item_info_cart(self, item_name):
        item_info = requests.get(url+'api/get_item_info_cart/'+item_name, json={"key": "value"})
        return item_info.json()

    def call_api_get_checkout_total(self):
        checkout_total = requests.get(url+'api/get_checkout_total/', json={"key": "value"})
        return checkout_total.json()['total']

    def call_api_post_add_item_to_store(self, item_name, price_per_unit, unit_type):
        item_dictionary = {"name":item_name, "price_per_unit": price_per_unit, "unit_type":unit_type}
        add_item_response = requests.post(url+'api/add_item_to_store/', data=json.dumps(item_dictionary), headers=headers)
        return self.call_api_get_item_info(item_name)

    def call_api_post_set_special_price(self, item_name, special):
        special_dictionary = {"item_name": item_name, "special": special}
        set_special_response = requests.post(url+'api/set_special_price/', data=json.dumps(special_dictionary), headers=headers)
        return self.call_api_get_item_info(item_name)

    def call_api_post_markdown_price(self, item_name, markdown_amount):
        markdown_dictionary = {"item_name": item_name, "markdown_price": markdown_amount}
        markdown_response = requests.post(url+'api/markdown_price/', data=json.dumps(markdown_dictionary), headers=headers)
        return self.call_api_get_item_info(item_name)

    def call_api_post_add_item_to_cart(self, item_name, quantity):
        cart_dictionary = {"name": item_name, "quantity": quantity}
        add_to_cart_response = requests.post(url+'api/add_item_to_cart/', data=json.dumps(cart_dictionary), headers=headers)
        return self.call_api_get_item_info_cart(item_name)

    def call_api_delete_from_store(self, item_name):
        delete_response = requests.delete(url+'api/delete_from_store/'+item_name, headers=headers)
        if delete_response.status_code == COMPLETED_NO_CONTENT:
            return True
        else:
            return False

    def call_api_delete_from_cart(self, item_name, quantity):
        delete_response = requests.delete(url+'api/delete_from_cart/'+item_name, data = json.dumps({"quantity": quantity}), headers=headers)
        if delete_response.status_code == COMPLETED_NO_CONTENT:
            return True
        else:
            return False

    def handle_user_input(self, user_input):
        return

    def run(self):
        while True:
            return
