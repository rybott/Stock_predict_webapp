from flask import Flask
from dotenv import load_dotenv
import os
import asyncio
from twscrape import API, gather

'''
async def add():
  api = API()
  await api.pool.add_account(os.environ['TW_Usr1'],os.environ['TW_XPW'],os.environ['TW_EM1'],os.environ['TW_EMPW1'])
  await api.pool.login_all()
asyncio.run(add())
'''
load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY']= os.environ['SECRET_KEY']

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/auth')



    return app

