from tests.utils import create_headers, load_decoded_response


def test_get_categories_valid(client):
    response = client.get(
        "/categories",
        headers=create_headers(),
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 200
    for category in json_response:
        assert all(key in category for key in ["id", "name", "description"]) is True
