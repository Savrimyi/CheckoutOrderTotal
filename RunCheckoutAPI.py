import unittest
import socketserver
import http.server
from CheckoutAPI import CheckoutAPI
import sys

HTTP_PORT = 8080

def run_tests():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('.', pattern='Test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

def run_api():
    httpd = socketserver.ThreadingTCPServer(('', HTTP_PORT),CheckoutAPI)

    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "run":
            run_api()
        elif sys.argv[1] =="test":
            run_tests()
        else:
            print("Invalid parameters")
    else:
        run_tests()
