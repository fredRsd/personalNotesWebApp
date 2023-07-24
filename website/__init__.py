from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

dataBase = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    webApp = Flask(__name__)
    webApp.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    webApp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    dataBase.init_app(webApp)

    from .views import views
    from .auth import auth

    webApp.register_blueprint(views, url_prefix='/')
    webApp.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with webApp.app_context():
        dataBase.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(webApp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return webApp


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        dataBase.create_all(app=app)
        print('Created Database!')
