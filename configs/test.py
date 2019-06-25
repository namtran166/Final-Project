from configs.base import Config


class TestConfig(Config):
    DEBUG = True
    secret_key = "test"
    pass
