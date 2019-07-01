from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

import main.models
from configs import config
from main.controllers.category import bp_category
from main.controllers.item import bp_item
from main.controllers.user import bp_auth, bp_user
from main.database import db
from main.utils.exception import BaseError

# Create our Flask app and update configurations
app = Flask(__name__)
app.config.from_object(config)

# Create the JWTManager instance to handle all authentication actions using JWT-token
jwt = JWTManager(app)
# Initialize our Flask app with this database setup
db.init_app(app)
# Create all the tables specified in this app
db.create_all(app=app)

# Register endpoints for our Flask app
app.register_blueprint(bp_category)
app.register_blueprint(bp_item)
app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)

# Register error handler for our Flask app
@app.errorhandler(BaseError)
def handle_customized_error(e):
    return e.messages()


@app.errorhandler(Exception)
def handle_general_error(*_):
    return jsonify(description="Unexpected Internal Server Error occurred."), 500
