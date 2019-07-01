import json
from tests.utils import load_decoded_response, create_headers


def register_user(client, information):
    response = client.post(
        "/users",
        headers=create_headers(),
        data=json.dumps(information)
    )
    json_response = load_decoded_response(response)
    return response, json_response


def authorize_user(client, authentication):
    response = client.post(
        "/auth",
        headers=create_headers(),
        data=json.dumps(authentication)
    )
    json_response = load_decoded_response(response)
    return response, json_response


def get_access_token(client, authentication):
    json_response = authorize_user(client, authentication)[1]
    return json_response['access_token']


def get_categories(client):
    response = client.get(
        "/categories",
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def get_category(client, category_id):
    response = client.get(
        "/categories/{}".format(category_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def post_categories(client, data):
    response = client.post(
        "/categories",
        headers=create_headers(),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


def get_items(client, category_id=None):
    response = client.get(
        "/categories/{}/items".format(category_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def get_item(client, category_id=None, item_id=None):
    response = client.get(
        "/categories/{}/items/{}".format(category_id, item_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def post_items(client, authentication=None, category_id=None, data=None):
    access_token = get_access_token(client, authentication)
    response = client.post(
        "/categories/{}/items".format(category_id),
        headers=create_headers(access_token=access_token),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


def delete_item(client, authentication=None, category_id=None, item_id=None):
    access_token = get_access_token(client, authentication)
    response = client.delete(
        "/categories/{}/items/{}".format(category_id, item_id),
        headers=create_headers(access_token=access_token)
    )
    return response


def put_item(client, authentication=None, category_id=None, item_id=None, data=None):
    access_token = get_access_token(client, authentication)
    response = client.put(
        "/categories/{}/items/{}".format(category_id, item_id),
        headers=create_headers(access_token=access_token),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response
