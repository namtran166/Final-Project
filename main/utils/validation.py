import functools

from flask import jsonify

from main.exception import CategoryNotFoundError, ItemNotFoundError, DuplicateUserError, UnauthorizedError
from main.models.category import CategoryModel
from main.models.item import ItemModel


def error_checking(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except CategoryNotFoundError as e:
            return e.message_return()
        except ItemNotFoundError as e:
            return e.message_return()
        except DuplicateUserError as e:
            return e.message_return()
        except UnauthorizedError as e:
            return e.message_return()
        except Exception:
            return jsonify(description="Internal Server Error"), 500

    return check_error


def validate_input(**kwargs):
    category = CategoryModel.find_by_id(kwargs['category_id'])
    if category is None:
        raise CategoryNotFoundError()
    if 'item_id' not in kwargs:
        return category
    item = ItemModel.find_by_id(kwargs['item_id'])
    if item is None:
        raise ItemNotFoundError()
    return item
