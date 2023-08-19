from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "predict_database.db"

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY']= 'odinfodfdpfom'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/auth')

    # Make sure you import all of those dependencies that you create
    from .models import User, Note

    create_database(app)

    return app

def create_database(app):
    if not path('website/'+ DB_NAME):
        db.create_all(app=app)
        print("Created Database")