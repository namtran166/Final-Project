import pytest

from tests.actions import register_user
from tests.utils import generate_random_string


@pytest.mark.parametrize(
    'authentication, status_code',
    [
        # Test case: Valid user
        (
                {
                    'username': 'brian124',
                    'password': '123456'
                },
                201
        ),
        # Test case: Valid user with space
        (
                {
                    'username': '    brian125  ',
                    'password': '    123456 '
                },
                201
        )
    ]
)
def test_post_users_valid(client, authentication, status_code):
    response, json_response = register_user(client, authentication)

    assert response.status_code == status_code
    assert all(key in json_response for key in ['id', 'username', 'first_name', 'last_name']) is True
    assert any(key in json_response for key in ['password', 'hashed_password']) is False


@pytest.mark.parametrize(
    'authentication, status_code, description',
    [
        # Test case: Incorrect data type for username
        (
                {
                    'username': 1,
                    'password': '123456'
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Incorrect data type for password
        (
                {
                    'username': 'brian124',
                    'password': 1
                },
                400,
                'Not a valid string.'
        ),
        # Test case: Username already exists
        (
                {
                    'username': 'brian123',
                    'password': '123456'
                },
                400,
                'Username already exists.'
        ),
        # Test case: Missing username
        (
                {
                    'password': '123356'
                },
                400,
                'Missing data for required field(s): username.'
        ),
        # Test case: Missing password
        (
                {
                    'username': 'brian123'
                },
                400,
                'Missing data for required field(s): password.'
        ),
        # Test case: Username is too short
        (
                {
                    'username': '  nam     ',
                    'password': '123456'
                },
                400,
                'A username must have between 6-64 characters.'
        ),
        # Test case: Password is too short
        (
                {
                    'username': '  brian123     ',
                    'password': '1234'
                },
                400,
                'A password must have between 6-64 characters.'
        ),
        # Test case: Username is too long
        (
                {
                    'username': generate_random_string(65),
                    'password': '123456'
                },
                400,
                'A username must have between 6-64 characters.'
        ),
        # Test case: Password is too long
        (
                {
                    'username': '  brian123     ',
                    'password': generate_random_string(65)
                },
                400,
                'A password must have between 6-64 characters.'
        ),
        # Test case: First name is too long
        (
                {
                    'username': '  brian123     ',
                    'password': '123456',
                    'first_name': generate_random_string(65)
                },
                400,
                'First name must be at most 32 characters.'
        ),
        # Test case: Last name is too long
        (
                {
                    'username': '  brian123     ',
                    'password': '123456',
                    'last_name': generate_random_string(65)
                },
                400,
                'Last name must be at most 32 characters.'
        )
    ]
)
def test_post_users_invalid(client, authentication, status_code, description):
    response, json_response = register_user(client, authentication)

    assert response.status_code == status_code
    assert json_response['description'] == description
