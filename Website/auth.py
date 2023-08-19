from flask import Blueprint

auth = Blueprint('auth', __name__)

# Budget_dummy
@auth.route('/budget', methods=['Get', 'Post'])
def budget():
    return "<h1>Login IN <h1>"

# Nutrition_dummy
@auth.route('/nutrition', methods=['Get', 'Post'])
def nutrition():
    return "<h1>Login IN <h1>"