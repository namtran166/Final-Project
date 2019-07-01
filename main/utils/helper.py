import functools

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError, DecodeError

from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.utils.exception import NotFoundError, UnauthorizedError, BadRequestError, ForbiddenError
from configs import config


def error_checking(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ForbiddenError, BadRequestError, UnauthorizedError, NotFoundError) as e:
            return e.messages()
        except Exception as e:
            print(e)
            print(e.__class__)
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


def generate_page_information(func):
    @functools.wraps(func)
    def wrapper(data=None, category_id=None, *args, **kwargs):
        items = ItemModel.query.filter_by(category_id=category_id)
        # Automatically return DEFAULT_PAGE if no specific page was requested
        if "page" not in data:
            data["page"] = config.DEFAULT_PAGE
        # Automatically set items per page to ITEMS_PER_PAGE if no per_page was specified
        if "per_page" not in data:
            data["per_page"] = config.ITEMS_PER_PAGE

        pagination = items.paginate(page=data["page"], per_page=data["per_page"], error_out=False)
        # If the requested page is too large, revert back to the maximum page
        if pagination.pages < data["page"]:
            pagination = items.paginate(page=pagination.pages, per_page=data["per_page"], error_out=False)

        cur_page = {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_items": pagination.total,
            "total_pages": pagination.pages,
            "items": pagination.items
        }
        return func(cur_page=cur_page, *args, **kwargs)

    return wrapper
