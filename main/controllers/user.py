from main.app import app


@app.route('/users', methods=['POST'])
def register_user():
    pass


@app.route('/auth', methods=['POST'])
def authenticate():
    pass
