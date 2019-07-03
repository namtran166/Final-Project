import functools

from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import DecodeError, ExpiredSignatureError, InvalidSignatureError

from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.utils.exception import NotFoundError, UnauthorizedError


def validate_item(func):
    """
    This function is provided two parameters: category_id and item_id.
    Check if this item exists in the provided category or not.
    :return: The item if it exists in the provided category. Raise a NotFoundError otherwise.
    """

    @functools.wraps(func)
    def check_item(*args, **kwargs):
        category = CategoryModel.find_by_id(kwargs['category_id'])
        if category is None:
            raise NotFoundError('Category not found.')
        item = ItemModel.find_by_id(kwargs['item_id'])
        if item is None or item.category_id != kwargs['category_id']:
            raise NotFoundError('Item not found.')
        return func(item=item, *args, **kwargs)

    return check_item


def validate_category(func):
    """
    This function is provided one parameter: category_id.
    Check if this category exists or not.
    :return: The category if it exists. Raise a NotFoundError otherwise.
    """

    @functools.wraps(func)
    def check_category(*args, **kwargs):
        category = CategoryModel.find_by_id(kwargs['category_id'])
        if category is None:
            raise NotFoundError('Category not found.')
        return func(category=category, *args, **kwargs)

    return check_category


def get_user_id(func):
    """
    Get user_id based on the provided jwt identity.
    :return: user_id if the access_token passed is valid. Raise an UnauthorizedError otherwise.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()['user']['id']
            return func(user_id=user_id, *args, **kwargs)
        except ExpiredSignatureError:
            raise UnauthorizedError('Access token has expired.')
        except (InvalidSignatureError, DecodeError, NoAuthorizationError):
            raise UnauthorizedError('Access token is invalid.')

    return wrapper


def load_data(schema):
    """
    Deserialize a request using a specified Schema
    :param schema: The Schema used to deserialize
    :return: the deserialized data
    """

    def wrapper(func):
        @functools.wraps(func)
        def second_wrapper(*args, **kwargs):
            data = schema().load(request.get_json()).data
            return func(data=data, *args, **kwargs)

        return second_wrapper

    return wrapper
