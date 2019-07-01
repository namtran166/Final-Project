from flask import Blueprint, jsonify

from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.utils.exception import BadRequestError, ForbiddenError
from main.utils.helper import error_checking, validate_category, validate_item, load_data, get_user_id

bp_item = Blueprint("item", __name__, url_prefix="/categories/<int:category_id>/items")


@bp_item.route("", methods=["GET"])
@error_checking
@validate_category
def get_items(**kwargs):
    items = ItemModel.query.filter_by(category_id=kwargs["category_id"]).all()
    return jsonify(ItemSchema(many=True, only=("id", "name", "description", "created", "user")).dump(items).data), 200


@bp_item.route("/<int:item_id>", methods=["GET"])
@error_checking
@validate_item
def get_item(item=None, **_):
    return jsonify(ItemSchema(only=("id", "name", "description", "created", "user")).dump(item).data), 200


@bp_item.route("", methods=["POST"])
@error_checking
@validate_category
@load_data(ItemSchema)
@get_user_id
def create_item(user_id=None, data=None, category_id=None, **_):
    if ItemModel.query.filter_by(name=data["name"], category_id=category_id, user_id=user_id).count() != 0:
        raise BadRequestError("You already have this item.")
    item = ItemModel(user_id=user_id, category_id=category_id, **data)
    item.save_to_db()
    return jsonify(ItemSchema(only=("id", "name", "description", "user")).dump(item).data), 201


@bp_item.route("/<int:item_id>", methods=["DELETE"])
@error_checking
@validate_item
@get_user_id
def delete_item(user_id=None, item=None, **_):
    if item.user_id != user_id:
        raise ForbiddenError("You don't have permission to do this.")
    item.delete_from_db()
    return jsonify({}), 204


@bp_item.route("/<int:item_id>", methods=["PUT"])
@error_checking
@validate_item
@load_data(ItemSchema)
@get_user_id
def update_item(user_id=None, data=None, item=None, **_):
    if item.user_id != user_id:
        raise ForbiddenError("You don't have permission to do this.")
    item.update_to_db(**data)
    return jsonify(ItemSchema().dump(item).data), 200
