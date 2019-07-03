import json
import random
import pytest

from tests.actions import get_access_token
from tests.utils import create_request_headers, generate_random_string, load_decoded_response, get_category_ids, get_item_ids


def put_item(client, authentication=None, category_id=None, item_id=None, data=None):
    access_token = get_access_token(client, authentication)
    response = client.put(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token=access_token),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    'authentication, category_id, item_id, data',
    [
        # Test case: Update successfully
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'name': 'Catch-22',
                    'description': 'Follows the life of Captain John Yossarian, a U.S. Army Air Forces B-25 bombardier.'
                }
        )
    ]
)
def test_put_item_valid(client, authentication, category_id, item_id, data):
    response, json_response = put_item(
        client, authentication=authentication, category_id=category_id, item_id=item_id, data=data)

    assert response.status_code == 200
    assert all(key in json_response for key in ['id', 'name', 'description', 'user', 'created', 'updated']) is True
    assert all(key in json_response['user'] for key in ['id', 'username']) is True


@pytest.mark.parametrize(
    'authentication, category_id, item_id, data, status_code, description',
    [
        # Test case: Incorrect data type for name
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'name': 1,
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for description
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'name': 'Catch-22',
                    'description': 1
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Missing name
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                400,
                'Missing data for required field(s): name.'
        ),
        # Test case: Name is too short
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'name': '     ',
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                400,
                'An item name must have between 1-256 characters.'
        ),
        # Test case: Name is too long
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'name': generate_random_string(257),
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                400,
                'An item name must have between 1-256 characters.'
        ),
        # Test case: Description is too long
        (
                {'username': 'brian123', 'password': '123456'},
                1,
                1,
                {
                    'name': '1984',
                    'description': generate_random_string(1025)
                },
                400,
                'An item description must have at most 1024 characters.'
        ),
        # Test case: Category not found
        (
                {'username': 'brian123', 'password': '123456'},
                max(get_category_ids())+1,
                random.choice(get_item_ids()),
                {
                    'name': '1984',
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                404,
                'Category not found.'
        ),
        # Test case: Item not found
        (
                {'username': 'brian123', 'password': '123456'},
                random.choice(get_category_ids()),
                max(get_item_ids())+1,
                {
                    'name': '1984',
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                404,
                'Item not found.'
        ),
        # Test case: Trying to update an item you do not own
        (
                {'username': 'brian456', 'password': '123456'},
                1,
                1,
                {
                    'name': '1984',
                    'description': 'A book about the risks of government overreach and totalitarianism.'
                },
                403,
                'You don\'t have permission to do this.'
        ),
    ]
)
def test_put_item_with_invalid_data(client, authentication, category_id, item_id, data, status_code, description):
    response, json_response = put_item(
        client, authentication=authentication, category_id=category_id, item_id=item_id, data=data)

    assert response.status_code == status_code
    assert json_response['description'] == description


@pytest.mark.parametrize(
    'access_token',
    [
        # Test case: Invalid access token
        generate_random_string(316),
        # Test case: Missing access token
        None
    ]
)
def test_put_item_with_invalid_token(client, access_token):
    response = client.delete(
        '/categories/{}/items/{}'.format(1, 1),
        headers=create_request_headers(access_token=access_token),
        data=json.dumps({
            'name': '1984',
            'description': 'A book about the risks of government overreach and totalitarianism.'
        })
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 401
    assert json_response['description'] == 'Access token is invalid.'
