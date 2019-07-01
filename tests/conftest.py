import pytest

from main import app
from main.database import db
from tests.database_setup import initialize_categories, initialize_users, drop_tables


@pytest.fixture
def app_testing():
    with app.app_context():
        initialize_categories()
        initialize_users()
    yield app
    drop_tables()
    db.create_all(app=app)


@pytest.fixture
def client(app_testing):
    return app_testing.test_client()