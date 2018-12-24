import unittest
import requests
import json

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
url = "http://localhost/"
OK = 200
CREATED = 201
NOT_FOUND = 404
BAD_REQUEST = 400
COMPLETED_NO_CONTENT = 204

class CheckoutAPITestCase(unittest.TestCase):

    def setUp(self):
        self.test_item = {"name": "bananas", "price_per_unit": 4, "unit_type": "per pound"}
        self.test_special = {"special": "buy 10 items, get 3 at %56 off"}
        self.test_markdown = {"item_name": "bananas", "markdown_price": 1.2}
        self.test_item_for_cart = {"name": "bananas", "quantity": 10}

    def test_add_item_to_store_POST(self):
        response = requests.post(url+'api/add_item_to_store/', data=json.dumps(self.test_item), headers=headers)
        self.assertEquals(reponse.status_code,CREATED)

    def test_add_item_without_data_POST(self):
        response = requests.post(url+'api/add_item_to_store/', headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_add_item_invalid_request_type(self):
        response = requests.get(url+'api/add_item_to_store/', data=json.dumps(self.test_item), headers=headers)
        self.assertEquals(response.status_code, NOT_FOUND)
        response = requests.put(url+'api/add_item_to_store/', data=json.dumps(self.test_item), headers=headers)
        self.assertEquals(response.status_code, NOT_FOUND)
        response = requests.delete(url+'api/add_item_to_store/', data=json.dumps(self.test_item), headers=headers)
        self.assertEquals(response.status_code, NOT_FOUND)

    def test_set_special_price_POST(self):
        response = requests.post(url+'api/set_special_price/', data=json.dumps(self.test_special), headers=headers)
        self.assertEquals(reponse.status_code,OK)

    def test_set_special_price_without_data_POST(self):
        response = requests.post(url+'api/set_special_price/', headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_set_special_price_invalid_request_type(self):
        response = requests.get(url+'api/set_special_price/', data=json.dumps(self.test_special), headers=headers)
        self.assertEquals(response.status_code, NOT_FOUND)
        response = requests.put(url+'api/set_special_price/', data=json.dumps(self.test_special), headers=headers)
        self.assertEquals(response.status_code, NOT_FOUND)
        response = requests.delete(url+'api/set_special_price/', data=json.dumps(self.test_special), headers=headers)
        self.assertEquals(response.status_code, NOT_FOUND)

    def test_markdown_price_POST(self):
        response = requests.post(url+'api/markdown_price/', data=json.dumps(self.test_markdown), headers=headers)
        self.assertEquals(reponse.status_code,OK)

    def test_markdown_without_data_POST(self):
        response = requests.post(url+'api/markdown_price/', headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_markdown_invalid_request_type(self):
        response = requests.get(url+'api/markdown_price/', data=json.dumps(self.test_markdown), headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/markdown_price/', data=json.dumps(self.test_markdown), headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/markdown_price/', data=json.dumps(self.test_markdown), headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_item_info_GET(self):
        response = requests.get(url+'api/get_item_info/'+test_item['name'], json={"key": "value"})
        self.assertEquals(reponse.status_code,OK)
        self.assertEquals(response.json(), test_item)

    def test_get_item_invalid_request_type(self):
        response = requests.post(url+'api/get_item_info/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/get_item_info/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/get_item_info/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_item_info_not_in_store(self):
        response = requests.get(url+'api/get_item_info/not a real item', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_remove_item_from_store_DELETE(self):
        response = requests.delete(url+'api/delete_from_store/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,COMPLETED_NO_CONTENT)

    def test_remove_item_not_in_store_DELETE(self):
        response = requests.delete(url+'api/delete_from_store/not a real item', headers=headers)
        self.assertEquals(reponse.status_code,BAD_REQUEST)

    def test_remove_item_invalid_request_type(self):
        response = requests.get(url+'api/delete_from_store/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.post(url+'api/delete_from_store/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/delete_from_store/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_items_in_store_GET(self):
        response = requests.get(url+'api/get_items_in_store/', json={"key": "value"})
        self.assertEquals(reponse.status_code,OK)
        self.assertEquals(response.json(), [test_item])

    def test_get_items_in_store_invalid_request_type(self):
        response = requests.post(url+'api/get_items_in_store/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/get_items_in_store/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/get_items_in_store/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_add_item_to_cart_POST(self):
        response = requests.post(url+'api/add_item_to_cart/', data=json.dumps(self.test_item_for_cart), headers=headers)
        self.assertEquals(reponse.status_code,CREATED)

    def test_add_items_to_cart_invalid_data_POST(self):
        response = requests.post(url+'api/add_item_to_cart/', headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_add_items_to_cart_invalid_request_type(self):
        response = requests.get(url+'api/add_item_to_cart/', data=json.dumps(self.test_item_for_cart), headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/add_item_to_cart/', data=json.dumps(self.test_item_for_cart), headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/add_item_to_cart/', data=json.dumps(self.test_item_for_cart), headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_items_in_cart_GET(self):
        response = requests.get(url+'api/get_items_in_cart/', json={"key": "value"})
        self.assertEquals(reponse.status_code,OK)

    def test_get_items_in_cart_invalid_request_type(self):
        response = requests.post(url+'api/get_items_in_cart/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/get_items_in_cart/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/get_items_in_cart/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_item_info_from_cart_GET(self):
        response = requests.get(url+'api/get_item_info_cart/'+test_item['name'], json={"key": "value"})
        self.assertEquals(reponse.status_code,OK)
        self.assertEquals(response.json(), test_item_for_cart)

    def test_get_item_info_from_cart_doesnt_exist(self):
        response = requests.get(url+'api/get_item_info_cart/not a real item', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_items_from_cart_invalid_request_type(self):
        response = requests.post(url+'api/get_item_info_cart/'+test_item['name'], json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/get_item_info_cart/'+test_item['name'], json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/get_item_info_cart/'+test_item['name'], json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_remove_item_from_cart_DELETE(self):
        response = requests.delete(url+'api/delete_from_cart/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,COMPLETED_NO_CONTENT)

    def test_remove_item_from_cart_doesnt_exist(self):
        response = requests.delete(url+'api/delete_from_cart/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_remove_item_from_cart_invalid_request_type(self):
        response = requests.post(url+'api/delete_from_cart/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.get(url+'api/delete_from_cart/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/delete_from_cart/'+test_item['name'], headers=headers)
        self.assertEquals(reponse.status_code,NOT_FOUND)

    def test_get_checkout_total(self):
        response = requests.get(url+'api/get_checkout_total/', json={"key": "value"})
        self.assertEquals(reponse.status_code,OK)

    def test_get_checkout_total_bad_request_type(self):
        response = requests.post(url+'api/get_checkout_total/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.put(url+'api/get_checkout_total/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
        response = requests.delete(url+'api/get_checkout_total/', json={"key": "value"})
        self.assertEquals(reponse.status_code,NOT_FOUND)
