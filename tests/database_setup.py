import json

from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

from configs import config
from main.models.category import CategoryModel
from main.models.item import ItemModel
from main.models.user import UserModel
from tests.actions import get_access_token
from tests.utils import create_headers


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


def initialize_items(client):
    items = [
        {
            "name": "1984",
            "description": "A book about the risks of government overreach and totalitarianism."
        },
        {
            "name": "Animal Farm",
            "description": "Reflects events leading up to the Russian Revolution of 1917."
        },
    ]
    authentication = {"username": "brian123", "password": "123456"}
    access_token = get_access_token(client, authentication)

    for item in items:
        client.post(
            '/categories/1/items',
            headers=create_headers(access_token=access_token),
            data=json.dumps(item)
        )


def drop_tables():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    ItemModel.__table__.drop(engine)
    CategoryModel.__table__.drop(engine)
    UserModel.__table__.drop(engine)
