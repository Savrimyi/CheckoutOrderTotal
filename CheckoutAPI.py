import socketserver
import http.server
import urllib.parse as urlparse
import json

from Checkout import Checkout

class CheckoutAPI(http.server.SimpleHTTPRequestHandler):
    """
        HTTP API Component, will accept HTTP requests to interact with Checkout and subsequently Item objects.
    """

    """ Handles GET requests """
    def do_GET(self):
        return

    """ Handles POST requests """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self.send_response(200)

    """ Handles DELETE requests """
    def do_DELETE(self):
        return

    """ Handles PUT requests """
    def do_PUT(self):
        return
