import functools

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError, DecodeError

from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.utils.exception import NotFoundError, UnauthorizedError, BadRequestError, ForbiddenError


def error_checking(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ForbiddenError, BadRequestError, UnauthorizedError, NotFoundError) as e:
            return e.messages()
        except Exception:
            return jsonify(description="Unexpected Internal Server Error occurred."), 500

    return check_error


def validate_item(func):
    @functools.wraps(func)
    def check_item(*args, **kwargs):
        category = CategoryModel.find_by_id(kwargs["category_id"])
        if category is None:
            raise NotFoundError("Category not found.")
        item = ItemModel.find_by_id(kwargs["item_id"])
        if item is None:
            raise NotFoundError("Item not found.")
        return func(item=item, *args, **kwargs)

    return check_item


def validate_category(func):
    @functools.wraps(func)
    def check_category(*args, **kwargs):
        category = CategoryModel.find_by_id(kwargs["category_id"])
        if category is None:
            raise NotFoundError("Category not found.")
        return func(category=category, *args, **kwargs)

    return check_category


def load_data(schema):
    def wrapper(func):
        @functools.wraps(func)
        def second_wrapper(*args, **kwargs):
            data = schema().load(request.get_json()).data
            return func(data=data, *args, **kwargs)

        return second_wrapper

    return wrapper


def get_user_id(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()["user"]["id"]
            return func(user_id=user_id, *args, **kwargs)
        except ExpiredSignatureError:
            raise UnauthorizedError("Access token has expired.")
        except (InvalidSignatureError, DecodeError, NoAuthorizationError):
            raise UnauthorizedError("Access token is invalid.")

    return wrapper
