from tests.actions import get_category


def test_get_category_valid(client):
    category_id = 1
    response, json_response = get_category(client, category_id)

    assert response.status_code == 200
    assert all(key in json_response for key in ["id", "name", "description", "items"]) is True
    assert type(json_response["items"]) is list


def test_get_category_invalid(client):
    category_id = 4
    response, json_response = get_category(client, category_id)

    assert response.status_code == 404
    assert json_response["description"] == "Category not found."
