from datetime import timedelta

from configs.base import Config


class DevelopmentConfig(Config):
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@127.0.0.1:3306/final_project_development"

    # Flask
    DEBUG = True

    # JWT-Extended
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)


config = DevelopmentConfig
