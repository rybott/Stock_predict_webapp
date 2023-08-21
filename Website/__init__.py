from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY']= 'odinfodfdpfom'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/auth')



    return app

