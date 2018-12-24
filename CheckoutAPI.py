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
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/get_items_in_store/' in self.path:
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/get_items_in_cart/' in self.path:
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/get_item_info_cart/' in self.path:
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/get_checkout_total/' in self.path:
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        else:
            self.send_response(NOT_FOUND)
            self.end_headers()
            return "Failed."

    """ Handles POST requests """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        #Use post data and call Checkout functions
        if '/api/add_item_to_store/' in self.path:
            self.send_response(CREATED)
            self.end_headers()
            return "Completed."
        elif '/api/set_special_price/' in self.path:
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/markdown_price/' in self.path:
            self.send_response(OK)
            self.end_headers()
            return "Completed."
        elif '/api/add_item_to_cart/' in self.path:
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
            return "Completed."
        elif '/api/delete_from_cart' in self.path:
            self.send_response(COMPLETED_NO_CONTENT)
            self.end_headers()
            return "Completed."
        else:
            self.send_response(NOT_FOUND)
            self.end_headers()
            return "Failed."

    """ Handles PUT requests (currently not using any, so always returns Error 404: NOT FOUND)"""
    def do_PUT(self):
        self.send_response(NOT_FOUND)
        self.end_headers()
        return "Failed."
