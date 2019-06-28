import pytest
import json
from tests.utils import create_headers, load_decoded_response, generate_random_string


@pytest.mark.parametrize(
    "data, status_code",
    [
        # Test case: Successfully create a new category
        (
                {
                    "name": "Fyodor Dostoyevsky",
                    "description": "19th-century Russian novelist."
                },
                201
        ),
    ]
)
def test_post_categories_valid(client, data, status_code):
    response = client.post(
        "/categories",
        headers=create_headers(),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == status_code
    assert all(key in json_response for key in ["id", "name", "description"]) is True


@pytest.mark.parametrize(
    "data, status_code, description",
    [
        # Test case: Missing name
        (
                {
                    "description": "19th-century Russian novelist."
                },
                400,
                "Missing data for required field: name."
        ),
        # Test case: Name is too short
        (
                {
                    "name": "      ",
                    "description": "19th-century Russian novelist."
                },
                400,
                "A category name must have must have at least 1 character."
        ),
        # Test case: Category name already exists
        (
                {
                    "name": "Joseph Hiller",
                    "description": "20th-century American author."
                },
                400,
                "Category already exists."
        )
    ]
)
def test_post_categories_invalid(client, data, status_code, description):
    response = client.post(
        "/categories",
        headers=create_headers(),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)

    assert response.status_code == status_code
    assert json_response["description"] == description
