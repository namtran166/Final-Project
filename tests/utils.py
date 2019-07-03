import json
from random import choice
from string import ascii_lowercase

from main import app
from main.database import db
from main.models.category import CategoryModel
from main.models.item import ItemModel


def get_item_ids():
    with app.app_context():
        item_ids = [item_id[0] for item_id in db.session.query(ItemModel.id).all()]
    return item_ids


def get_category_ids():
    with app.app_context():
        category_ids = [category_id[0] for category_id in db.session.query(CategoryModel.id).all()]
    return category_ids


def create_request_headers(access_token=None):
    header = {'Content-Type': 'application/json'}
    if access_token:
        header['Authorization'] = 'Bearer {}'.format(access_token)
    return header


def load_decoded_response(response):
    return json.loads(response.data.decode('utf-8'))


def generate_random_string(length):
    return ''.join(choice(ascii_lowercase) for _ in range(length))
