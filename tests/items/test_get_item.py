import pytest

from tests.actions import get_item
from tests.database_setup import initialize_items


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
