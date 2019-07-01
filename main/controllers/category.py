from flask import Blueprint, jsonify

from main.models.category import CategoryModel
from main.schemas.category import CategorySchema
from main.utils.exception import BadRequestError
from main.utils.helper import error_checking, validate_category, load_data

bp_category = Blueprint("category", __name__, url_prefix="/categories")


@bp_category.route("", methods=['GET'])
@error_checking
def get_categories():
    categories = CategoryModel.query.all()
    return jsonify(CategorySchema(many=True, only=("id", "name", "description")).dump(categories).data), 200


@bp_category.route("/<int:category_id>", methods=['GET'])
@error_checking
@validate_category
def get_category(category=None, **_):
    return jsonify(CategorySchema().dump(category).data), 200


@bp_category.route("", methods=['POST'])
@error_checking
@load_data(CategorySchema)
def create_category(data=None):
    if CategoryModel.query.filter_by(name=data["name"]).first():
        raise BadRequestError("Category already exists.")
    category = CategoryModel(**data)
    category.save_to_db()
    return jsonify(CategorySchema().dump(category).data), 201
