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

    """ Makes a request to the API to get information about an item. """
    def call_api_get_item_info(self, item_name):
        item = requests.get(url+'api/get_item_info/'+item_name, json={"key": "value"}, headers=headers)
        if item.status_code == NOT_FOUND: return None
        return item.json()

    """ Makes a request to the API to get a list of items for sale in the store. """
    def call_api_get_items_in_store(self):
        items_in_store = requests.get(url+'api/get_items_in_store/', json={"key": "value"})
        if items_in_store.status_code == NOT_FOUND: return None
        return items_in_store.json()['items_in_store']

    """ Makes a request to the API to get a list of items in the customer's cart. """
    def call_api_get_items_in_cart(self):
        items_in_cart = requests.get(url+'api/get_items_in_cart/', json={"key": "value"})
        if items_in_cart.status_code == NOT_FOUND: return None
        return items_in_cart.json()['items_in_cart']

    """ Makes a request to the API to get information about an item in the cart. """
    def call_api_get_item_info_cart(self, item_name):
        item_info = requests.get(url+'api/get_item_info_cart/'+item_name, json={"key": "value"})
        if item_info.status_code == NOT_FOUND: return None
        return item_info.json()

    """ Makes a request to the API to get the checkout total. """
    def call_api_get_checkout_total(self):
        checkout_total = requests.get(url+'api/get_checkout_total/', json={"key": "value"})
        if checkout_total.status_code == NOT_FOUND: return None
        return checkout_total.json()['total']

    """ Makes a request to the API to add an item to the store. """
    def call_api_post_add_item_to_store(self, item_name, price_per_unit, unit_type):
        item_dictionary = {"name":item_name, "price_per_unit": price_per_unit, "unit_type":unit_type}
        add_item_response = requests.post(url+'api/add_item_to_store/', data=json.dumps(item_dictionary), headers=headers)
        if add_item_response.status_code == NOT_FOUND: return None
        return self.call_api_get_item_info(item_name)

    """ Makes a request to the API to set a special price for an item in the store. """
    def call_api_post_set_special_price(self, item_name, special):
        special_dictionary = {"item_name": item_name, "special": special}
        set_special_response = requests.post(url+'api/set_special_price/', data=json.dumps(special_dictionary), headers=headers)
        if set_special_response.status_code == NOT_FOUND: return None
        return self.call_api_get_item_info(item_name)

    """ Makes a request to the API to mark down the price of an item in the store. """
    def call_api_post_markdown_price(self, item_name, markdown_amount):
        markdown_dictionary = {"item_name": item_name, "markdown_price": markdown_amount}
        markdown_response = requests.post(url+'api/markdown_price/', data=json.dumps(markdown_dictionary), headers=headers)
        if markdown_response.status_code == NOT_FOUND: return None
        return self.call_api_get_item_info(item_name)

    """ Makes a request to the API to add an item to the customer's cart. """
    def call_api_post_add_item_to_cart(self, item_name, quantity):
        cart_dictionary = {"name": item_name, "quantity": quantity}
        add_to_cart_response = requests.post(url+'api/add_item_to_cart/', data=json.dumps(cart_dictionary), headers=headers)
        if add_to_cart_response.status_code == NOT_FOUND: return None
        return self.call_api_get_item_info_cart(item_name)

    """ Makes a request to the API to delete an item from the store. """
    def call_api_delete_from_store(self, item_name):
        delete_response = requests.delete(url+'api/delete_from_store/'+item_name, headers=headers)
        if delete_response.status_code == COMPLETED_NO_CONTENT:
            return True
        else:
            return False

    """ Makes a request to the API to remove an item from the customer's cart. """
    def call_api_delete_from_cart(self, item_name, quantity):
        delete_response = requests.delete(url+'api/delete_from_cart/'+item_name, data = json.dumps({"quantity": quantity}), headers=headers)
        if delete_response.status_code == COMPLETED_NO_CONTENT:
            return True
        else:
            return False

    """ Takes user input and calls functions above to interact with the API. """
    def handle_user_input(self, user_input):
        user_input = user_input.lower()
        if user_input == "help" or user_input == "?":
            self.print_help_menu()
        elif user_input == "add item":
            item_name = input("Item Name: ")
            price_per_unit = int(input("Price per Unit: "))
            unit_type = input("Unit Type [each | per pound]: ")
            item = self.call_api_post_add_item_to_store(item_name, price_per_unit, unit_type)
            if item is None:
                print("Unable to add item. Check store to see if it is already in stock.")
            else:
                print("Item Added.", item)
        elif user_input == "delete item":
            item_name = input("Item Name: ")
            result = self.call_api_delete_from_store(item_name)
            if result:
                print("Item deleted.")
            else:
                print("Item not found!")
        elif user_input == "markdown":
            item_name = input("Item Name: ")
            markdown_amount = float(input("Markdown Amount: "))
            item = self.call_api_post_markdown_price(item_name, markdown_amount)
            if item is None:
                print("Item not found!")
            else:
                print("Markdown applied. ", item)
        elif user_input == "special":
            item_name = input("Item Name: ")
            special = input("Special: ")
            item = self.call_api_post_set_special_price(item_name, special)
            print("Special applied. ", item)
        elif user_input == "item info store":
            item_name = input("Item Name: ")
            item = self.call_api_get_item_info(item_name)
            if item is None:
                print("Item not found!")
            else:
                print(item)
        elif user_input == "get store":
            items = self.call_api_get_items_in_store()
            print("Items for sale: ", items)
        elif user_input == "scan item":
            item_name = input("Item Name: ")
            quantity = float(input("Quantity: "))
            result = self.call_api_post_add_item_to_cart(item_name, quantity)
            if result is None:
                print("Item not found!")
            else:
                print("%d %s added to cart." % (quantity, item_name))
        elif user_input == "remove item":
            item_name = input("Item Name: ")
            quantity = float(input("Quantity: "))
            result = self.call_api_delete_from_cart(item_name, quantity)
            if result:
                print("%d %s removed from cart." % (quantity, item_name))
            else:
                print("Item not found!")
        elif user_input == "item info cart":
            item_name = input("Item Name: ")
            item = self.call_api_get_item_info_cart(item_name)
            if item is not None:
                print(item)
            else:
                print("Item not found!")
        elif user_input == "get cart":
            items = self.call_api_get_items_in_cart()
            print("Items in cart: ", items)
        elif user_input == "total":
            total = self.call_api_get_checkout_total()
            print("Total: ", total)
        else:
            print("Command not recognized. Try 'help' to see a list of commands.")

    """ Runs continuously accepting user input and handling API calls. """
    def run(self):
        while True:
            try:
                user_input = input("Enter a command: ")
                self.handle_user_input(user_input)
                print()
            except Exception as e:
                print("Invalid input.")

    """ Prints the help menu. """
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

""" Allows the program to be run interactively. """
if __name__ == '__main__':

    point_of_sale = PointOfSale()
    point_of_sale.print_help_menu()
    point_of_sale.run()
