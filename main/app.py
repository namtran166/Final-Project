from flask import Flask

app = Flask(__name__)


@app.before_first_request
def create_tables():
    db.create_all(app=app)


if __name__ == '__main__':
    from main.database import db

    db.init_app(app)
    app.run(port=5001, debug=True)
