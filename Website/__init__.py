from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'odinfodfdpfom'

    from .dashboard import dashboard
    from .data import data

    app.register_blueprint(dashboard, url_prefix= '/')
    app.register_blueprint(data, url_prefix= '/')

    return app