import socketserver
import http.server
import urllib.parse as urlparse
import json

from Checkout import Checkout

OK = 200
CREATED = 201
NOT_FOUND = 404
COMPLETED_NO_CONTENT = 204

class CheckoutAPI(http.server.SimpleHTTPRequestHandler):
    """
        HTTP API Component, will accept HTTP requests to interact with Checkout and subsequently Item objects.
    """
    checkout = Checkout()
    """ Handles GET requests """
    def do_GET(self):
        #Parse path and call Checkout functions
        if '/api/get_item_info/' in self.path:
            item_name = self.path.split('/')[2]
            item_info = self.checkout.get_item_information(item_name)
            #Turn into JSON and send back
            self.send_response(OK)
            self.end_headers()
            return item_info.json()
        elif '/api/get_items_in_store/' in self.path:
            #items_list = self.checkout.get_items_in_store()
            items_list = self.checkout.get_store_as_json()
            #Turn into JSON and send back
            self.send_response(OK)
            self.end_headers()
            return items_list
        elif '/api/get_items_in_cart/' in self.path:
            #items_list = self.checkout.get_items_in_cart()
            items_list = self.checkout.get_cart_as_json()
            #Turn into JSON and send back
            self.send_response(OK)
            self.end_headers()
            return items_list
        elif '/api/get_item_info_cart/' in self.path:
            item_name = self.path.split('/')[2]
            item_info = self.checkout.get_item_information_from_cart(item_name)
            #Turn into JSON and send back
            self.send_response(OK)
            self.end_headers()
            return item_info.json()
        elif '/api/get_checkout_total/' in self.path:
            checkout_total = self.checkout.get_checkout_total()
            #Turn into JSON and send back
            self.send_response(OK)
            self.end_headers()
            return json.dumps({"total": checkout_total})
        else:
            self.send_response(NOT_FOUND)
            self.end_headers()
            return "Failed."

    """ Handles POST requests """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        if post_data is not None and post_data != b'':
            post_dict = json.loads(post_data)
            print(post_dict)
        else:
            self.send_response(NOT_FOUND)
            self.end_headers()
            return "Failed."
        #Use post data and call Checkout functions
        if '/api/add_item_to_store/' in self.path:
            #Get item info from POST
            action_result = self.checkout.add_item_to_store(post_dict['name'],post_dict['price_per_unit'],post_dict['unit_type'])
            #If action completed normally, send CREATED response, else BAD_REQUEST
            self.send_response(CREATED)
            self.end_headers()
            return "Completed."
        elif '/api/set_special_price/' in self.path:
            #Get item info from POST
            action_result = self.checkout.get_item_information(post_dict['item_name']).set_special_price(post_dict['special'])
            #If action completed normally, send CREATED response, else BAD_REQUEST
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/markdown_price/' in self.path:
            #Get item info from POST
            action_result = self.checkout.get_item_information(post_dict['item_name']).markdown_price(post_dict['markdown_price'])
            #If action completed normally, send CREATED response, else BAD_REQUEST
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/add_item_to_cart/' in self.path:
            #Get item info from POST
            action_result = self.checkout.add_item_to_cart(post_dict['name'],post_dict['quantity'])
            #If action completed normally, send CREATED response, else BAD_REQUEST
            self.send_response(CREATED)
            self.end_headers()
            return "Completed."
        else:
            self.send_response(NOT_FOUND)
            self.end_headers()
            return "Failed."

    """ Handles DELETE requests """
    def do_DELETE(self):

        #Get data and call functions, handle errors
        if '/api/delete_from_store/' in self.path:
            self.send_response(COMPLETED_NO_CONTENT)
            self.end_headers()
            return ""
        elif '/api/delete_from_cart' in self.path:
            self.send_response(COMPLETED_NO_CONTENT)
            self.end_headers()
            return ""
        else:
            self.send_response(NOT_FOUND)
            self.end_headers()
            return "Failed."

    """ Handles PUT requests (currently not using any, so always returns Error 404: NOT FOUND)"""
    def do_PUT(self):
        self.send_response(NOT_FOUND)
        self.end_headers()
        return "Failed."
