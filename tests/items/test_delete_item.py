import pytest

from tests.actions import get_access_token
from tests.database_setup import initialize_items
from tests.utils import create_headers, load_decoded_response


def delete_item(client, authentication=None, category_id=None, item_id=None):
    access_token = get_access_token(client, authentication)
    response = client.delete(
        "/categories/{}/items/{}".format(category_id, item_id),
        headers=create_headers(access_token=access_token)
    )
    return response


def test_delete_item_valid(client):
    initialize_items(client)
    authentication = {"username": "brian123", "password": "123456"}
    response = delete_item(client, authentication=authentication, category_id=1, item_id=1)

    assert response.status_code == 204


@pytest.mark.parametrize(
    "authentication, category_id, item_id, status_code, description",
    [
        # Test case: Category not found
        (
                {"username": "brian123", "password": "123456"},
                4,
                1,
                404,
                "Category not found."
        ),
        # Test case: Item not found
        (
                {"username": "brian123", "password": "123456"},
                1,
                4,
                404,
                "Item not found."
        ),
        # Test case: Trying to delete an item you do not own
        (
                {"username": "brian456", "password": "123456"},
                1,
                1,
                403,
                "You don't have permission to do this."
        ),
    ]
)
def test_delete_item_with_invalid_data(client, authentication, category_id, item_id, status_code, description):
    initialize_items(client)
    response = delete_item(client, authentication=authentication, category_id=category_id, item_id=item_id)
    json_response = load_decoded_response(response)

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
def test_delete_item_with_invalid_token(client, access_token):
    initialize_items(client)
    response = client.delete(
        "/categories/{}/items/{}".format(1, 1),
        headers=create_headers(access_token=access_token)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 401
    assert json_response["description"] == "Access token is invalid."
