import datetime

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from main.models.item import ItemModel
from main.utils.controllers import item_with_user_information, items_with_user_information, item_with_user_and_date
from main.utils.exception import BadRequestError, ForbiddenError
from main.utils.validation import error_checking, validate_input, retrieve_and_validate_input

bp_item = Blueprint("item", __name__, url_prefix="/categories/<int:category_id>/items")


@bp_item.route("", methods=["GET"])
@error_checking
def get_items(category_id):
    validate_input(category_id=category_id)
    items = ItemModel.get_items_by_category_id(category_id)
    return jsonify(items_with_user_information(items)), 200


@bp_item.route("/<int:item_id>", methods=["GET"])
@error_checking
def get_item(category_id, item_id):
    item = validate_input(category_id=category_id, item_id=item_id)
    return jsonify(item_with_user_information(item)), 200


@bp_item.route("", methods=["POST"])
@error_checking
@jwt_required
def create_item(category_id):
    _, user_id, create_data = retrieve_and_validate_input(category_id=category_id)
    if ItemModel.duplicate_item_exists(create_data["name"], category_id, user_id):
        raise BadRequestError("You already have this item.")

    item = ItemModel(user_id=user_id, category_id=category_id, **create_data)
    item.save_to_db()
    return jsonify(item_with_user_information(item)), 201


@bp_item.route("/<int:item_id>", methods=["DELETE"])
@error_checking
@jwt_required
def delete_item(category_id, item_id):
    item = validate_input(category_id=category_id, item_id=item_id)
    user_id = get_jwt_identity()["user"]["id"]

    if item.user_id != user_id:
        raise ForbiddenError("You don't have permission to do this.")

    item.delete_from_db()
    return jsonify({}), 204


@bp_item.route("/<int:item_id>", methods=["PUT"])
@error_checking
@jwt_required
def update_item(category_id, item_id):
    item, user_id, update_data = retrieve_and_validate_input(category_id=category_id, item_id=item_id)
    if item.user_id != user_id:
        raise ForbiddenError("You don't have permission to do this.")

    item.update_to_db(**update_data)
    return jsonify(item_with_user_and_date(item)), 200
