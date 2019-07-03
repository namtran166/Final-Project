import pytest
import json

from tests.utils import create_request_headers, generate_random_string, load_decoded_response


def post_categories(client, data):
    response = client.post(
        '/categories',
        headers=create_request_headers(),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    'data, status_code',
    [
        # Test case: Successfully create a new category
        (
                {
                    'name': 'Fyodor Dostoyevsky',
                    'description': '19th-century Russian novelist.'
                },
                201
        ),
    ]
)
def test_post_categories_valid(client, data, status_code):
    response, json_response = post_categories(client, data)

    assert response.status_code == status_code
    assert all(key in json_response for key in ['id', 'name', 'description', 'items']) is True
    assert json_response['items'] == []


@pytest.mark.parametrize(
    'data, status_code, description',
    [
        # Test case: Incorrect data type for name
        (
                {
                    'name': 1,
                    'description': '19th-century Russian novelist.'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for name
        (
                {
                    'name': "Fyodor",
                    'description': 1
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Missing name
        (
                {
                    'description': '19th-century Russian novelist.'
                },
                400,
                'Missing data for required field(s): name.'
        ),
        # Test case: Name is too short
        (
                {
                    'name': '      ',
                    'description': '19th-century Russian novelist.'
                },
                400,
                'A category name must have between 1-256 characters.'
        ),
        # Test case: Name is too long
        (
                {
                    'name': generate_random_string(257),
                    'description': '19th-century Russian novelist.'
                },
                400,
                'A category name must have between 1-256 characters.'
        ),
        # Test case: Description is too long
        (
                {
                    'name': 'Fyodor Dostoevsky',
                    'description': generate_random_string(1025)
                },
                400,
                'A category description must have at most 1024 characters.'
        ),
        # Test case: Category name already exists
        (
                {
                    'name': 'Joseph Hiller',
                    'description': '20th-century American author.'
                },
                400,
                'Category already exists.'
        )
    ]
)
def test_post_categories_invalid(client, data, status_code, description):
    response, json_response = post_categories(client, data)

    assert response.status_code == status_code
    assert json_response['description'] == description
