from tests.actions import get_items
from tests.database_setup import initialize_items


def test_get_items_valid(client):
    initialize_items(client)
    response, json_response = get_items(client, category_id=1)

    assert response.status_code == 200
    assert type(json_response) is list
    for category in json_response:
        assert all(key in category for key in ["id", "name", "description", "user"]) is True
        assert all(key in category["user"] for key in ["id", "username"]) is True


def test_get_items_invalid(client):
    response, json_response = get_items(client, category_id=4)

    assert response.status_code == 404
    assert json_response["description"] == "Category not found."
