from tests.utils import create_headers, load_decoded_response, generate_random_string


def test_get_category_valid(client):
    category_id = 1
    response = client.get(
        "/categories/{}".format(category_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 200
    assert all(key in json_response for key in ["id", "name", "description"]) is True


def test_get_category_invalid(client):
    category_id = 4
    response = client.get(
        "/categories/{}".format(category_id),
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 404
    assert json_response["description"] == "Category not found."
