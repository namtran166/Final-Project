from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from main.exception import DuplicateUserError, UnauthorizedError
from main.models.user import UserModel
from main.schemas.user import UserSchema, AuthenticationSchema
from main.utils.validation import error_checking

bp_user = Blueprint("user", __name__, url_prefix="/users")
bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_user.route("", methods=['POST'])
@error_checking
def register_user():
    data = UserSchema().load(request.get_json()).data
    username = data["username"].strip()
    password = data["password"].strip()

    if UserModel.find_by_username(username):
        raise DuplicateUserError

    hashed_password = generate_password_hash(password)
    data["username"] = username
    data["hashed_password"] = hashed_password
    del data["password"]
    user = UserModel(**data)
    user.save_to_db()
    return jsonify(UserSchema().dump(user).data), 200


@bp_auth.route("", methods=['POST'])
@error_checking
def authenticate():
    data = AuthenticationSchema().load(request.get_json()).data
    username = data["username"].strip()
    password = data["password"].strip()

    user = UserModel.find_by_username(username)

    if user and check_password_hash(user.hashed_password, password):
        access_token = create_access_token(identity={"user": UserSchema().dump(user).data})
        authentication = UserSchema().dump(user).data
        authentication["access_token"] = access_token
        return jsonify(authentication), 200

    raise UnauthorizedError
