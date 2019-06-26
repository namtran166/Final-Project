from flask import jsonify


class _Exception(Exception):
    status_code = None
    message = {}

    def __init__(self):
        super(Exception).__init__()

    def message_return(self):
        return jsonify(description=self.message), self.status_code


class DuplicateCategoryError(_Exception):
    status_code = 400
    message = "Category already exists."


class DuplicateItemError(_Exception):
    status_code = 400
    message = "You already have this item. Cannot create a new item with the same name."


class DuplicateUserError(_Exception):
    status_code = 400
    message = "Username already exists."


class UnauthorizedError(_Exception):
    status_code = 401
    message = "Invalid Credentials."


class ForbiddenError(_Exception):
    status_code = 403
    message = "You don't have permission to do this."


class CategoryNotFoundError(_Exception):
    status_code = 404
    message = "Category not found."


class ItemNotFoundError(_Exception):
    status_code = 404
    message = "Item not found."


class InternalServerError(_Exception):
    status_code = 500
    message = "An unexpected Internal Server Error occurred."
