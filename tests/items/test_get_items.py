import pytest

from tests.utils import create_request_headers, load_decoded_response, get_category_ids


def get_items(client, url):
    response = client.get(
        url,
        headers=create_request_headers()
    )
    json_response = load_decoded_response(response)
    return response, json_response


@pytest.mark.parametrize(
    'url',
    [
        # Test case: Get items with valid page
        (
                'categories/1/items?page=1&per_page=2'
        ),
        # Test case: Page requested exceeds number of pages, revert back to the maximum page
        (
                'categories/1/items?page=100&per_page=2'
        ),
        # Test case: No page requested, automatically return page number 1
        (
                'categories/1/items?per_page=2'
        ),
        # Test case: Items per page is missing, automatically set it to 20
        (
                'categories/1/items?page=1'
        )
    ]
)
def test_get_items_valid(client, url):
    response, json_response = get_items(client, url=url)

    assert response.status_code == 200
    assert all(key in json_response for key in ['page', 'per_page', 'total_items', 'total_pages']) is True
    for category in json_response['items']:
        assert all(key in category for key in ['id', 'name', 'description', 'user']) is True
        assert all(key in category['user'] for key in ['id', 'username']) is True


@pytest.mark.parametrize(
    'url, status_code, description',
    [
        # Test case: Incorrect data type for page parameter
        (
                'categories/1/items?page="1"&per_page=2',
                400,
                'Not a valid integer.'
        ),
        # Test case: Incorrect data type for per page parameter
        (
                'categories/1/items?page=1&per_page="2"',
                400,
                'Not a valid integer.'
        ),
        # Test case: Category does not exist
        (
                'categories/{}/items?page=1&per_page=2'.format(max(get_category_ids())+1),
                404,
                'Category not found.'
        ),
        # Test case: Page is too small
        (
                'categories/1/items?page=0&per_page=2',
                400,
                'Requested page must be positive.'
        ),
        # Test case: Item per page is too small
        (
                'categories/1/items?page=1&per_page=0',
                400,
                'One page can only display between 1-100 items.'
        ),
        # Test case: Item per page is too big
        (
                'categories/1/items?page=1&per_page=101',
                400,
                'One page can only display between 1-100 items.'
        )
    ]
)
def test_get_items_invalid(client, url, status_code, description):
    response, json_response = get_items(client, url=url)

    assert response.status_code == status_code
    assert json_response['description'] == description
