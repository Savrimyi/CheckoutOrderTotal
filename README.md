# Checkout Order Total Kata

## Item.py
The Item object stores information about a given item in the store. It holds the name, price per unit, type of unit cost, special deals, and markdown conditions of the item.

## Checkout.py
The Checkout object interacts with Item objects to maintain the store for the cashier. The Checkout will allow the cashier to add items to the store, scan items for a customer, and get a total cost of goods sold.

## CheckoutAPI.py
The CheckoutAPI is an HTTP wrapper for the Checkout object. It allows a remote terminal to interact with a Checkout server. For this example, only one client will be used, but this could easily be extended with an API token and login requirement to allow multiple cashiers to use the single store system simultaneously.

### Running the API
The API is run with the RunCheckoutAPI.py file.
The command to run the API is: 'python[3.7] RunCheckoutAPI.py run'
This will run the API on port 8080 by default. This is configurable in the RunCheckoutAPI.py file.

## PointOfSale.py
This component is how the user can interact with the API via command line interface. It simply takes user input and makes API calls via HTTP on their behalf. This allows them a simple way to configure items in the store and perform customer-facing actions such as scanning items and retrieving the total cost.

### Running the PointOfSale system
You can run the program with the following command:
    'python[3.7] PointOfSale.py'

The following commands are used to interact with the API via the PointOfSale system:
    'help' - Print the help menu.
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

Note: The API must be running for the PointOfSale system to function properly.

## Requirements
This project was built using the latest version of Python (3.7.1). In my environment the command to run python 3.7 is 'python3.7' but if no other python is installed, you can simply use 'python'. Other python3 variants should work, but 2 will not.
If you are on a mac, you can install this version using Brew.
The only external library required is Requests.
You can install it with the command: 'pip[3.7] install requests'.
Alternatively, you can use the requirements.txt file included in the project by using the command: 'pip[3.7] install -r requirements.txt'

## Testing
Tests are named with the structure 'Test*.py' and are cumulatively run by the RunCheckoutAPI.py file.
Command to run the tests: 'python[3.7] RunCheckoutAPI.py' or 'python[3.7] RunCheckoutAPI.py test'

Note: The tests will not work properly if the API is not running on localhost:8080 (this may be reconfigured in the TestAPI.py file).
See instructions above to run the API.

I recommend running the API and tests in separate windows, but you can run the API in the background instead if that is better for your environment.

### List of commands to reproduce my results:
      1. python3.7 RunCheckoutAPI.py run &
      2. python3.7 RunCheckoutAPI.py test
      3. python3.7 PointOfSale.py
      4. ps aux | grep RunCheckoutAPI.py
      5. kill -9 <PID of RunCheckoutAPI.py>

You can skip steps 4 and 5, but the API will continue running in the background until it is stopped. If you run the API and tests in separate windows, these steps will be unnecessary.
