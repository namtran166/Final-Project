from flask import Blueprint, jsonify

from configs import config
from main.models.item import ItemModel
from main.schemas.item import ItemSchema
from main.schemas.pagination import ItemPaginationSchema
from main.utils.exception import BadRequestError, ForbiddenError
from main.utils.helper import get_user_id, load_data, validate_category, validate_item

bp_item = Blueprint("item", __name__, url_prefix="/categories/<int:category_id>/items")


@bp_item.route("", methods=["GET"])
@validate_category
@load_data(ItemPaginationSchema)
def get_items(data, **kwargs):
    # Automatically return DEFAULT_PAGE if no specific page was requested
    if "page" not in data:
        data["page"] = config.DEFAULT_PAGE
    # Automatically set items per page to DEFAULT_ITEMS_PER_PAGE if no per_page was specified
    if "per_page" not in data:
        data["per_page"] = config.DEFAULT_ITEMS_PER_PAGE

    items = ItemModel.query.filter_by(category_id=kwargs["category_id"])
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
    return jsonify(ItemPaginationSchema().dump(cur_page).data), 200


@bp_item.route("/<int:item_id>", methods=["GET"])
@validate_item
def get_item(item, **_):
    return jsonify(ItemSchema(only=("id", "name", "description", "created", "user")).dump(item).data), 200


@bp_item.route("", methods=["POST"])
@validate_category
@load_data(ItemSchema)
@get_user_id
def create_item(user_id, data, category_id, **_):
    if ItemModel.query.filter_by(name=data["name"], category_id=category_id, user_id=user_id).count() != 0:
        raise BadRequestError("You already have this item.")
    item = ItemModel(user_id=user_id, category_id=category_id, **data)
    item.save_to_db()
    return jsonify(ItemSchema(only=("id", "name", "description", "user")).dump(item).data), 201


@bp_item.route("/<int:item_id>", methods=["DELETE"])
@validate_item
@get_user_id
def delete_item(user_id, item, **_):
    if item.user_id != user_id:
        raise ForbiddenError("You don't have permission to do this.")
    item.delete_from_db()
    return jsonify({}), 204


@bp_item.route("/<int:item_id>", methods=["PUT"])
@validate_item
@load_data(ItemSchema)
@get_user_id
def update_item(user_id, data, item, **_):
    print(_)
    print(data)
    if item.user_id != user_id:
        raise ForbiddenError("You don't have permission to do this.")
    item.update_to_db(**data)
    return jsonify(ItemSchema().dump(item).data), 200
