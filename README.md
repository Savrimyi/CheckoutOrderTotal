# Checkout Order Total Kata

## Item.py
The Item object stores information about a given item in the store. It holds the name, price per unit, type of unit cost, special deals, and markdown conditions of the item. 

## Checkout.py
The Checkout object interacts with Item objects to maintain the store for the cashier. The Checkout will allow the cashier to add items to the store, scan items for a customer, and get a total cost of goods sold. 

## CheckoutAPI.py
The CheckoutAPI is an HTTP wrapper for the Checkout object. It allows a remote terminal to interact with a Checkout server. For this example, only one client will be used, but this could easily be extended with an API token and login requirement to allow multiple cashiers to use the single store system simultaneously. 

## Requirements
This project was built using the latest version of Python (3.7.1).
If you are on a mac, you can install this version using Brew. 
The only external library required is Requests. 
You can install it with the command: 'pip[3.7] install requests'.
Alternatively, you can use the requirements.txt file included in the project by using the command: 'pip[3.7] install -r requirements.txt'

## Testing
Tests are named with the structure 'Test*.py' and are cumulatively run by the RunCheckoutAPI.py file. 
Command to run the tests: 'python[3.7] RunCheckoutAPI.py' or 'python[3.7] RunCheckoutAPI.py test'

# Running the API
The API is also run with the RunCheckoutAPI.py file. 
The command to run the API is: 'python[3.7] RunCheckoutAPI.py run'
This will run the API on port 8080 by default. This is configurable in the RunCheckoutAPI.py file. 


