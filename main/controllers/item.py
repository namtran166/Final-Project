from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from main.exception import DuplicateItemError, ForbiddenError
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.utils.validation import error_checking, validate_input

bp_item = Blueprint("item", __name__, url_prefix="/categories/<int:category_id>/items")


@bp_item.route("", methods=['GET'])
@error_checking
def get_items(category_id):
    validate_input(category_id=category_id)
    items = ItemModel.get_items_by_category_id(category_id)
    return jsonify(ItemSchema(many=True).dump(items).data), 200


@bp_item.route("/<int:item_id>", methods=['GET'])
@error_checking
def get_item(category_id, item_id):
    item = validate_input(category_id=category_id, item_id=item_id)
    return jsonify(ItemSchema().dump(item).data), 200


@bp_item.route("", methods=['POST'])
@jwt_required
def create_item(category_id):
    validate_input(category_id=category_id)

    user_id = get_jwt_identity()["user"]["id"]
    data = ItemSchema().load(request.get_json()).data

    if ItemModel.duplicate_item_exists(data["name"], category_id, user_id):
        raise DuplicateItemError

    item = ItemModel(user_id=user_id, category_id=category_id, **data)
    item.save_to_db()
    return jsonify(ItemSchema().dump(item).data)


@bp_item.route("/<int:item_id>", methods=['DELETE'])
@jwt_required
def delete_item(category_id, item_id):
    item = validate_input(category_id=category_id, item_id=item_id)

    user_id = get_jwt_identity()["user"]["id"]

    if item.user_id != user_id:
        raise ForbiddenError

    item.delete_from_db()
    return jsonify(ItemSchema().dump(item).data)


@bp_item.route("/<int:item_id>", methods=['PUT'])
@jwt_required
def update_item(category_id, item_id):
    item = validate_input(category_id=category_id, item_id=item_id)

    user_id = get_jwt_identity()["user"]["id"]
    data = ItemSchema().load(request.get_json()).data

    if item.user_id != user_id:
        raise ForbiddenError

    item.update_to_db(**data)
    item.save_to_db()
    return jsonify(ItemSchema().dump(item).data)
