from main.app import app


@app.route('/categories', methods=['GET'])
def get_categories():
    pass


@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    pass


@app.route('/categories', methods=['POST'])
def create_category():
    pass
