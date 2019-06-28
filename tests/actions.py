import json
from tests.tester import Tester
from tests.utils import load_decoded_response, create_headers


def _tester_register(client, authentication):
    tester = Tester(client)
    response = tester.register(authentication)
    json_response = load_decoded_response(response)
    return response, json_response


def _tester_authorize(client, authentication):
    tester = Tester(client)
    response = tester.authorize(authentication)
    json_response = load_decoded_response(response)
    return response, json_response


def initialize_items(client):
    items = [
        {
            "name": "1984",
            "description": "A book about the risks of government overreach and totalitarianism."
        },
        {
            "name": "Animal Farm",
            "description": "Reflects events leading up to the Russian Revolution of 1917."
        },
    ]

    authentication = {"username": "brian123", "password": "123456"}

    tester = Tester(client)
    access_token = tester.get_access_token(authentication)
    for item in items:
        client.post(
            '/categories/1/items',
            headers=create_headers(access_token=access_token),
            data=json.dumps(item)
        )
