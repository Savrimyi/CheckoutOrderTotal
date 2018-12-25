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
        user_input = user_input.lower()
        if user_input == "help" or user_input == "?":
            self.print_help_menu()
        elif user_input == "add item":
            item_name = input("Item Name: ")
            price_per_unit = int(input("Price per Unit: "))
            unit_type = input("Unit Type [each | per pound]: ")
            item = self.call_api_post_add_item_to_store(item_name, price_per_unit, unit_type)
            print("Item Added.", item)
        elif user_input == "delete item":
            item_name = input("Item Name: ")
            self.call_api_delete_from_store(item_name)
            print("Item deleted.")
        elif user_input == "markdown":
            item_name = input("Item Name: ")
            markdown_amount = int(input("Markdown Amount: "))
            item = self.call_api_post_markdown_price(item_name, markdown_amount)
            print("Markdown applied. ", item)
        elif user_input == "special":
            item_name = input("Item Name: ")
            special = input("Special: ")
            item = self.call_api_post_set_special_price(item_name, special)
            print("Special applied. ", item)
        elif user_input == "item info store":
            item_name = input("Item Name: ")
            item = self.call_api_get_item_info(item_name)
            print(item)
        elif user_input == "get store":
            items = self.call_api_get_items_in_store()
            print("Items for sale: ", items)
        elif user_input == "scan item":
            item_name = input("Item Name: ")
            quantity = int(input("Quantity: "))
            self.call_api_post_add_item_to_cart(item_name, quantity)
            print("%d %s added to cart." % (quantity, item_name))
        elif user_input == "remove item":
            item_name = input("Item Name: ")
            quantity = int(input("Quantity: "))
            self.call_api_delete_from_cart(item_name, quantity)
            print("%d %s removed from cart." % (quantity, item_name))
        elif user_input == "item info cart":
            item_name = input("Item Name: ")
            item = self.call_api_get_item_info_cart(item_name)
            print(item)
        elif user_input == "get cart":
            items = self.call_api_get_items_in_cart()
            print("Items in cart: ", items)
        elif user_input == "total":
            total = self.call_api_get_checkout_total()
            print("Total: ", total)
        else:
            print("Command not recognized. Try 'help' to see a list of commands.")

    def run(self):
        while True:
            user_input = input("Enter a command: ")
            self.handle_user_input(user_input)
            print()

    def print_help_menu(self):
        help_menu = """
                    You may use the following commands to interact with the Point of Sale system:
                        'help' - Print this menu.
                        'add item' - Add an item to the store.
                        'delete item' - Delete an item from the store.
                        'markdown' - Markdown the price of an item.
                        'special' - Add a special discount to an item.
                        'item info store' - Get information about an item.
                        'get store' - Get a list of items for sale in the store.
                        'scan item' - Scan an item to add it to the customer's cart.
                        'remove item' - Remove an item from the customer's cart.
                        'item info cart' - Get information about an item in the customer's cart.
                        'get cart' - Get a list of items in the customer's cart.
                        'total' - Get the checkout total.
                    """
        print(help_menu)

if __name__ == '__main__':

    point_of_sale = PointOfSale()
    point_of_sale.print_help_menu()
    point_of_sale.run()
