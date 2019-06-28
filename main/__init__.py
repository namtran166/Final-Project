from flask import Flask
from flask_jwt_extended import JWTManager

import main.models
from configs import config
from main.controllers.category import bp_category
from main.controllers.item import bp_item
from main.controllers.user import bp_user, bp_auth
from main.database import db

app = Flask(__name__)
app.config.from_object(config)
jwt = JWTManager(app)
db.init_app(app)
db.create_all(app=app)

app.register_blueprint(bp_category)
app.register_blueprint(bp_item)
app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)
