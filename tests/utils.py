import json

from random import choice
from string import ascii_lowercase
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

from configs import config
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel


def create_headers(access_token=None):
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = "Bearer {}".format(access_token)
    return headers


def load_decoded_response(response):
    return json.loads(response.data.decode("utf-8"))


def generate_random_string(length):
    return ''.join(choice(ascii_lowercase) for _ in range(length))


def initialize_categories():
    categories = [
        {
            "name": "George Orwell",
            "description": "19th-century English novelist and essayist."
        },
        {
            "name": "Joseph Hiller",
            "description": "20th-century American author."
        },
        {
            "name": "Stephen King",
            "description": "21st-century Maine, American novelist."
        }
    ]
    for category in categories:
        category_object = CategoryModel(**category)
        category_object.save_to_db()


def initialize_users():
    users = [
        {
            "username": "brian123",
            "password": "123456",
            "first_name": "Nam",
            "last_name": "Tran"
        },
        {
            "username": "brian456",
            "password": "123456",
            "first_name": "Quan",
            "last_name": "Chau"
        }
    ]
    for user in users:
        hashed_password = generate_password_hash(user["password"])
        user["hashed_password"] = hashed_password
        del user["password"]
        user_object = UserModel(**user)
        user_object.save_to_db()


def drop_tables():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    ItemModel.__table__.drop(engine)
    CategoryModel.__table__.drop(engine)
    UserModel.__table__.drop(engine)
