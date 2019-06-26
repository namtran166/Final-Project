from flask import Blueprint, jsonify, request

from main.exception import DuplicateCategoryError
from main.models.category import CategoryModel
from main.schemas.category import CategorySchema
from main.utils.validation import error_checking, validate_input

bp_category = Blueprint("category", __name__, url_prefix="/categories")


@bp_category.route("", methods=['GET'])
@error_checking
def get_categories():
    categories = CategoryModel.get_all_categories()
    return jsonify(CategorySchema(many=True).dump(categories).data)


@bp_category.route("/<int:category_id>", methods=['GET'])
@error_checking
def get_category(category_id):
    category = validate_input(category_id=category_id)
    return jsonify(CategorySchema().dump(category).data)


@bp_category.route("", methods=['POST'])
@error_checking
def create_category():
    data = CategorySchema().load(request.get_json()).data

    if CategoryModel.find_by_name(data["name"]):
        raise DuplicateCategoryError

    category = CategoryModel(**data)
    category.save_to_db()
    return jsonify(CategorySchema().dump(category).data)
