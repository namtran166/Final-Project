from datetime import timedelta


class Config:
    # SQL Alchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask
    SECRET_KEY = "brian@gotitapp.co"

    # JWT-Extended
    JWT_SECRET_KEY = "namtran166"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
