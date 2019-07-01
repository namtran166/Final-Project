import pytest
import json

from tests.database_setup import initialize_items
from tests.utils import create_headers, load_decoded_response


def get_items(client, category_id=None, data=None):
    response = client.get(
        "/categories/{}/items".format(category_id),
        headers=create_headers(),
        data=json.dumps(data)
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    "data",
    [
        # Test case: Get items with valid page
        (
                {"page": 1, "per_page": 2}
        ),
        # Test case: Page requested exceeds number of pages, revert back to the maximum page
        (
                {"page": 3, "per_page": 2}
        ),
        # Test case: No page requested, automatically return page number 1
        (
                {"per_page": 2}
        ),
        # Test case: Items per page is missing, automatically set it to 20
        (
                {"page": 1}
        )
    ]
)
def test_get_items_valid(client, data):
    initialize_items(client)
    response, json_response = get_items(client, category_id=1, data=data)

    assert response.status_code == 200
    assert all(key in json_response for key in ["page", "per_page", "total_items", "total_pages"]) is True
    for category in json_response["items"]:
        assert all(key in category for key in ["id", "name", "description", "user"]) is True
        assert all(key in category["user"] for key in ["id", "username"]) is True


@pytest.mark.parametrize(
    "category_id, data, status_code, description",
    [
        # Test case: Category does not exist
        (
                4,
                {"page": 1, "per_page": 2},
                404,
                "Category not found."
        ),
        # Test case: Page is too small
        (
                1,
                {"page": 0, "per_page": 2},
                400,
                "Requested page must be positive."
        ),
        # Test case: Item per page is too small
        (
                1,
                {"page": 1, "per_page": 0},
                400,
                "One page can only display between 1-100 items."
        ),
        # Test case: Item per page is too big
        (
                1,
                {"page": 1, "per_page": 101},
                400,
                "One page can only display between 1-100 items."
        )
    ]
)
def test_get_items_invalid(client, category_id, data, status_code, description):
    response, json_response = get_items(client, category_id=category_id, data=data)

    assert response.status_code == status_code
    assert json_response["description"] == description
