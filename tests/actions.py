from tests.tester import Tester
from tests.utils import load_decoded_response


def tester_register(client, authentication):
    tester = Tester(client)
    response = tester.register(authentication)
    json_response = load_decoded_response(response)
    return response, json_response


def tester_authorize(client, authentication):
    tester = Tester(client)
    response = tester.authorize(authentication)
    json_response = load_decoded_response(response)
    return response, json_response
