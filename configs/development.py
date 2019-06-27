from configs.base import Config
from datetime import timedelta


class DevelopmentConfig(Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@127.0.0.1:3306/final_project_development"

    # Flask
    DEBUG = True

    # JWT-Extended
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)


config = DevelopmentConfig
