from flask import Blueprint

data = Blueprint('data', __name__)

@data.route('/login')
def login():
    return "<h1>Login IN <h1>"


@data.route('/logout')
def logout():
    return "<h1>Logout<h1>"


@data.route('/signup')
def signup():
    return "<p>signup<p>"