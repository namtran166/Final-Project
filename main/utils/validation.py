import functools

from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.utils.exception import NotFoundError, UnauthorizedError, BadRequestError, ForbiddenError


def error_checking(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ForbiddenError, BadRequestError, UnauthorizedError, NotFoundError) as e:
            return e.messages()
        except Exception as e:
            return jsonify(description="Unexpected Internal Server Error occured.".format(e)), 500

    return check_error


def validate_input(**kwargs):
    category = CategoryModel.find_by_id(kwargs['category_id'])
    if category is None:
        raise NotFoundError("Category not found.")
    if 'item_id' not in kwargs:
        return category
    item = ItemModel.find_by_id(kwargs['item_id'])
    if item is None:
        raise NotFoundError("Item not found.")
    return item


@jwt_required
def retrieve_and_validate_input(**kwargs):
    category_or_item = validate_input(**kwargs)
    user_id = get_jwt_identity()["user"]["id"]
    data = ItemSchema().load(request.get_json()).data
    return category_or_item, user_id, data
