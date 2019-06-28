from tests.utils import create_headers, load_decoded_response


def test_get_categories_valid(client):
    category_id = 1
    response = client.get(
        "/categories/{}/items".format(category_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 200
    assert type(json_response) is list
    for category in json_response:
        assert all(key in category for key in ["id", "name", "description", "user"]) is True
        assert all(key in category["user"] for key in ["id", "username"]) is True


def test_get_categories_invalid(client):
    category_id = 4
    response = client.get(
        "/categories/{}/items".format(category_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 404
    assert json_response["description"] == "Category not found."
