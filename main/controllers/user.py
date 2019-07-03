from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from main.models.user import UserModel
from main.schemas.user import UserSchema, UserAuthenticationSchema
from main.utils.exception import BadRequestError, UnauthorizedError
from main.utils.helper import load_data

bp_user = Blueprint('user', __name__, url_prefix='/users')
bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_user.route('', methods=['POST'])
@load_data(UserSchema)
def register_user(data):
    if UserModel.find_by_username(data['username']):
        raise BadRequestError('Username already exists.')

    # Generate a hashed password for this user from provided password
    hashed_password = generate_password_hash(data['password'])
    data['hashed_password'] = hashed_password
    del data['password']

    user = UserModel(**data)
    user.save_to_db()
    return jsonify(UserSchema().dump(user).data), 201


@bp_auth.route('', methods=['POST'])
@load_data(UserAuthenticationSchema)
def authorize_user(data):
    user = UserModel.find_by_username(data['username'])

    if user and check_password_hash(user.hashed_password, data['password']):
        user_in_jwt_token = UserSchema(only=('id', 'username')).dump(user).data
        access_token = create_access_token(identity={'user': user_in_jwt_token})
        authentication = {
            'access_token': access_token,
            'user': user
        }
        return jsonify(UserAuthenticationSchema().dump(authentication).data), 200
    raise UnauthorizedError('Invalid Credentials.')
