import pytest

from main import app
from main.database import db
from tests.database_setup import drop_tables, initialize_categories, initialize_users


@pytest.fixture
def app_setup():
    drop_tables()
    db.create_all(app=app)
    with app.app_context():
        initialize_categories()
        initialize_users()
    return app


@pytest.fixture
def client(app_setup):
    return app_setup.test_client()
