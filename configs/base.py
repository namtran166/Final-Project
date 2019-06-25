class Config(object):
    DEBUG = False

    # SQL Alchemy
    SQLALCHEMY_DATABASE_URI = "mysql://namtran166:1234@localhost:6789/database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    secret_key = "configuration"
    pass
