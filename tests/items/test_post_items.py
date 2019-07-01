import json

import pytest

from tests.actions import post_items
from tests.database_setup import initialize_items
from tests.utils import create_headers, load_decoded_response, generate_random_string


@pytest.mark.parametrize(
    "authentication, category_id, data",
    [
        # Test case: Book name does not exist
        (
                {"username": "brian123", "password": "123456"},
                1,
                {
                    "name": "Catch-22",
                    "description": "Follows the life of Captain John Yossarian, a U.S. Army Air Forces B-25 bombardier."
                }
        ),
        # Test case: Book name does exist, but belongs to other user
        (
                {"username": "brian456", "password": "123456"},
                1,
                {
                    "name": "Animal Farm",
                    "description": "Reflects events leading up to the Russian Revolution of 1917."
                }
        ),
        # Test case: Book name does exist, belongs to you but different category
        (
                {"username": "brian123", "password": "123456"},
                2,
                {
                    "name": "Animal Farm",
                    "description": "Reflects events leading up to the Russian Revolution of 1917."
                }
        )
    ]
)
def test_post_items_valid(client, authentication, category_id, data):
    initialize_items(client)
    response, json_response = post_items(client, authentication=authentication, category_id=category_id, data=data)

    assert response.status_code == 201
    assert all(key in json_response for key in ["id", "name", "description", "user"]) is True
    assert all(key in json_response["user"] for key in ["id", "username"]) is True


@pytest.mark.parametrize(
    "authentication, category_id, data, status_code, description",
    [
        # Test case: Missing name
        (
                {"username": "brian123", "password": "123456"},
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
                {
                    "name": "1984",
                    "description": generate_random_string(1025)
                },
                400,
                "An item description must have at most 1024 characters."
        ),
        # Test case: Item already exists
        (
                {"username": "brian123", "password": "123456"},
                1,
                {
                    "name": "1984",
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                400,
                "You already have this item."
        ),
        # Test case: Category not found
        (
                {"username": "brian123", "password": "123456"},
                4,
                {
                    "name": "1984",
                    "description": "A book about the risks of government overreach and totalitarianism."
                },
                404,
                "Category not found."
        ),
    ]
)
def test_post_items_with_invalid_data(client, authentication, category_id, data, status_code, description):
    initialize_items(client)
    response, json_response = post_items(client, authentication=authentication, category_id=category_id, data=data)

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
def test_post_items_with_invalid_token(client, access_token):
    response = client.post(
        "/categories/{}/items".format(1),
        headers=create_headers(access_token=access_token),
        data=json.dumps({
            "name": "1984",
            "description": "A book about the risks of government overreach and totalitarianism."
        })
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 401
    assert json_response["description"] == "Access token is invalid."
