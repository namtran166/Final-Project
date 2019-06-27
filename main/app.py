from flask import Flask
from flask_jwt_extended import JWTManager

from main.controllers.category import bp_category
from main.controllers.item import bp_item
from main.controllers.user import bp_user, bp_auth
from configs import config


app = Flask(__name__)
app.config.from_object(config)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.register_blueprint(bp_category)
app.register_blueprint(bp_item)
app.register_blueprint(bp_user)
app.register_blueprint(bp_auth)

if __name__ == '__main__':
    from main.database import db

    db.init_app(app)
    app.run(port=5000)
