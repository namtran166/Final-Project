from tests.actions import get_categories


def test_get_categories_valid(client):
    response, json_response = get_categories(client)

    assert response.status_code == 200
    for category in json_response:
        assert all(key in category for key in ["id", "name", "description"]) is True
