import importlib
import os

env = os.getenv("FLASK_ENV", "development")

config = importlib.import_module('configs.' + env).config
