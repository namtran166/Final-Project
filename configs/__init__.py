import os
import importlib

env = os.getenv("FLASK_ENV", "development")

config = importlib.import_module('configs.' + env).config
