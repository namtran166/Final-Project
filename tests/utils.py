import json

from random import choice
from string import ascii_lowercase


def create_headers(access_token=None):
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = "Bearer {}".format(access_token)
    return headers


def load_decoded_response(response):
    return json.loads(response.data.decode("utf-8"))


def generate_random_string(length):
    return ''.join(choice(ascii_lowercase) for _ in range(length))

