from tests.utils import create_request_headers, load_decoded_response, get_category_ids
import random


def get_category(client, category_id):
    response = client.get(
        '/categories/{}'.format(category_id),
        headers=create_request_headers(),
    )
    json_response = load_decoded_response(response)
    return response, json_response


def test_get_category_valid(client):
    category_id = random.choice(get_category_ids())
    response, json_response = get_category(client, category_id)

    assert response.status_code == 200
    assert all(key in json_response for key in ['id', 'name', 'description', 'items']) is True
    assert type(json_response['items']) is list


def test_get_category_invalid(client):
    category_id = max(get_category_ids())+1
    response, json_response = get_category(client, category_id)

    assert response.status_code == 404
    assert json_response['description'] == 'Category not found.'
