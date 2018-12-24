import unittest
import socketserver
import http.server
from CheckoutAPI import CheckoutAPI
import sys

HTTP_PORT = 8080


"""Runs the unit tests."""
def run_tests():
    tests = unittest.TestLoader().discover('.', pattern='Test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

""" Runs the HTTP API on port 8080. """
def run_api():
    httpd = socketserver.ThreadingTCPServer(('', HTTP_PORT),CheckoutAPI)

    httpd.serve_forever()

""" Runs the code as an application, if not imported into another program """
if __name__ == '__main__':

    #Simple command line parameter parsing to handle test and run conditions.
    if len(sys.argv) == 2:
        if sys.argv[1] == "run":
            run_api()
        elif sys.argv[1] =="test":
            run_tests()
        else:
            print("Invalid parameters")
    else:
        run_tests()
