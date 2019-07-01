import pytest

from tests.database_setup import initialize_items
from tests.utils import create_headers, load_decoded_response


def get_item(client, category_id=None, item_id=None):
    response = client.get(
        "/categories/{}/items/{}".format(category_id, item_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def test_get_item_valid(client):
    initialize_items(client)
    response, json_response = get_item(client, category_id=1, item_id=1)

    assert response.status_code == 200
    assert type(json_response) is dict
    assert all(key in json_response for key in ["id", "name", "description", "user", "created"]) is True
    assert all(key in json_response["user"] for key in ["id", "username"]) is True


@pytest.mark.parametrize(
    "category_id, item_id, status_code, description",
    [
        # Test case: Category not found
        (
                4,
                1,
                404,
                "Category not found."
        ),
        # Test case: Item not found
        (
                3,
                10,
                404,
                "Item not found."
        ),
    ]
)
def test_get_item_invalid(client, category_id, item_id, status_code, description):
    initialize_items(client)
    response, json_response = get_item(client, category_id=category_id, item_id=item_id)

    assert response.status_code == status_code
    assert json_response["description"] == description
