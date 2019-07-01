import json

import pytest

from tests.actions import get_access_token
from tests.database_setup import initialize_items
from tests.utils import create_headers, generate_random_string, load_decoded_response


def put_item(client, authentication=None, category_id=None, item_id=None, data=None):
    access_token = get_access_token(client, authentication)
    response = client.put(
        "/categories/{}/items/{}".format(category_id, item_id),
        headers=create_headers(access_token=access_token),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    "authentication, category_id, item_id, data",
    [
        # Test case: Update successfully
        (
                {"username": "brian123", "password": "123456"},
                1,
                1,
                {
                    "name": "Catch-22",
                    "description": "Follows the life of Captain John Yossarian, a U.S. Army Air Forces B-25 bombardier."
                }
        )
    ]
)
def test_put_item_valid(client, authentication, category_id, item_id, data):
    initialize_items(client)
    response, json_response = put_item(
        client, authentication=authentication, category_id=category_id, item_id=item_id, data=data)

    assert response.status_code == 200
    assert all(key in json_response for key in ["id", "name", "description", "user", "created", "updated"]) is True
    assert all(key in json_response["user"] for key in ["id", "username"]) is True


@pytest.mark.parametrize(
    "authentication, category_id, item_id, data, status_code, description",
    [
        # Test case: Missing name
        (
                {"username": "brian123", "password": "123456"},
                1,
                1,
                {
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                400,
                "Missing data for required field: name."
        ),
        # Test case: Name is too short
        (
                {"username": "brian123", "password": "123456"},
                1,
                1,
                {
                    "name": "     ",
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                400,
                "An item name must have between 1-256 characters."
        ),
        # Test case: Name is too long
        (
                {"username": "brian123", "password": "123456"},
                1,
                1,
                {
                    "name": generate_random_string(257),
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                400,
                "An item name must have between 1-256 characters."
        ),
        # Test case: Description is too long
        (
                {"username": "brian123", "password": "123456"},
                1,
                1,
                {
                    "name": "1984",
                    "description": generate_random_string(1025)
                },
                400,
                "An item description must have at most 1024 characters."
        ),
        # Test case: Category not found
        (
                {"username": "brian123", "password": "123456"},
                4,
                1,
                {
                    "name": "1984",
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                404,
                "Category not found."
        ),
        # Test case: Item not found
        (
                {"username": "brian123", "password": "123456"},
                1,
                4,
                {
                    "name": "1984",
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                404,
                "Item not found."
        ),
        # Test case: Trying to update an item you do not own
        (
                {"username": "brian456", "password": "123456"},
                1,
                1,
                {
                    "name": "1984",
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                403,
                "You don't have permission to do this."
        ),
    ]
)
def test_put_item_with_invalid_data(client, authentication, category_id, item_id, data, status_code, description):
    initialize_items(client)
    response, json_response = put_item(
        client, authentication=authentication, category_id=category_id, item_id=item_id, data=data)

    assert response.status_code == status_code
    assert json_response["description"] == description


@pytest.mark.parametrize(
    "access_token",
    [
        # Test case: Invalid access token
        1,
        # Test case: Missing access token
        None
    ]
)
def test_put_item_with_invalid_token(client, access_token):
    initialize_items(client)
    response = client.delete(
        "/categories/{}/items/{}".format(1, 1),
        headers=create_headers(access_token=access_token),
        data=json.dumps({
            "name": "1984",
            "description": "A book about the risks of government overreach and totalitarianism."
        })
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 401
    assert json_response["description"] == "Access token is invalid."
