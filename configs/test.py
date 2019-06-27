from configs.base import Config


class TestConfig(Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@127.0.0.1:3306/final_project_test"

    # Flask
    DEBUG = False

    # PyTest
    TESTING = True


config = TestConfig
