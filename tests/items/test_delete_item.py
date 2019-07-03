import pytest
import random
from tests.actions import get_access_token
from tests.utils import create_request_headers, load_decoded_response, get_category_ids, get_item_ids, generate_random_string


def delete_item(client, authentication=None, category_id=None, item_id=None):
    access_token = get_access_token(client, authentication)
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token=access_token)
    )
    return response


def test_delete_item_valid(client):
    authentication = {'username': 'brian123', 'password': '123456'}
    response = delete_item(client, authentication=authentication, category_id=1, item_id=1)

    assert response.status_code == 204


@pytest.mark.parametrize(
    'authentication, category_id, item_id, status_code, description',
    [
        # Test case: Category not found
        (
                {'username': 'brian123', 'password': '123456'},
                max(get_category_ids())+1,
                random.choice(get_item_ids()),
                404,
                'Category not found.'
        ),
        # Test case: Item not found
        (
                {'username': 'brian123', 'password': '123456'},
                random.choice(get_category_ids()),
                max(get_item_ids())+1,
                404,
                'Item not found.'
        ),
        # Test case: Trying to delete an item you do not own
        (
                {'username': 'brian456', 'password': '123456'},
                1,
                random.choice(get_item_ids()),
                403,
                'You don\'t have permission to do this.'
        ),
    ]
)
def test_delete_item_with_invalid_data(client, authentication, category_id, item_id, status_code, description):
    response = delete_item(client, authentication=authentication, category_id=category_id, item_id=item_id)
    json_response = load_decoded_response(response)

    assert response.status_code == status_code
    assert json_response['description'] == description


@pytest.mark.parametrize(
    'access_token',
    [
        # Test case: Invalid access token
        generate_random_string(316),
        # Test case: Missing access token
        None
    ]
)
def test_delete_item_with_invalid_token(client, access_token):
    category_id = 1
    item_id = random.choice(get_item_ids())
    response = client.delete(
        '/categories/{}/items/{}'.format(category_id, item_id),
        headers=create_request_headers(access_token=access_token)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == 401
    assert json_response['description'] == 'Access token is invalid.'
