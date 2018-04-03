import json
import requests
import unittest

with open("../config.json") as json_data:
    config = json.load(json_data)

host = str(config["host"])
port = str(config["port"])
url_load = 'http://' + host + ':' + port + '/api/roles/load'

headers = {'content-type': 'application/json'}


class MyTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_role_loading(self):
        payload = {"userId": "csoda@yodafone.hu"}
        r = requests.post(url_load, data=json.dumps(payload), headers=headers)
        response = r.json()
        expected_response = {"roles": ["padavan", "yoda"]}
        self.assertEqual(response, expected_response)

    def test_not_existing_role_loading(self):
        payload = {"userId": "wrong@yodafone.hu"}
        r = requests.post(url_load, data=json.dumps(payload), headers=headers)
        response = r.json()
        expected_response = {"roles": []}
        self.assertEqual(response, expected_response)