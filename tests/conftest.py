import pytest

from main import app
from main.database import db
from tests.database_setup import drop_tables, initialize_categories, initialize_users


@pytest.fixture
def app_testing():
    drop_tables()
    db.create_all(app=app)
    with app.app_context():
        initialize_categories()
        initialize_users()
    return app


@pytest.fixture
def client(app_testing):
    return app_testing.test_client()
