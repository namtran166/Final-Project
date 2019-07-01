from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from main.models.user import UserModel
from main.schemas.user import UserSchema
from main.utils.exception import BadRequestError, UnauthorizedError
from main.utils.helper import error_checking, load_data

bp_user = Blueprint("user", __name__, url_prefix="/users")
bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_user.route("", methods=['POST'])
@error_checking
@load_data(UserSchema)
def register_user(data=None):
    if UserModel.find_by_username(data["username"]):
        raise BadRequestError("Username already exists.")

    # Generate a hashed password for this user from provided password
    hashed_password = generate_password_hash(data["password"])
    data["hashed_password"] = hashed_password
    del data["password"]

    user = UserModel(**data)
    user.save_to_db()
    return jsonify(UserSchema().dump(user).data), 201


@bp_auth.route("", methods=['POST'])
@error_checking
@load_data(UserSchema)
def authorize_user(data=None):
    user = UserModel.find_by_username(data["username"])

    if user and check_password_hash(user.hashed_password, data["password"]):
        user = UserSchema().dump(user).data
        access_token = create_access_token(identity={"user": user})
        user["access_token"] = access_token
        return jsonify(user), 200

    raise UnauthorizedError("Invalid Credentials.")
