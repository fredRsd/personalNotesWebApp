from flask import Flask #Flask imported
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy imported
from os import path #for handling paths and directories
from flask_login import LoginManager    #handling authorizations

DATABASE_NAME = "database.db" #database file's name/ address
appDataBase = SQLAlchemy() #SQLAlchemy is used for database

def makeApp():  #the web app
    from .views import views #views blueprint is imported from views.py (different views of the site)
    from .auth import authBP  #auth blueprint is imported from auth.py (authorization process)
    from .models import User, Note  #User and Notes clases imported from models

    webApp = Flask(__name__)   # An instance of Flask created and assigned to app variable
    webApp.config['SECRET_KEY'] = 'abc09ghi'   # Secret key for cryptographic purposes
    webApp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_NAME}' #dataBase URI set using f-string
    appDataBase.init_app(webApp)   #SQLAlchemy initialized
    webApp.register_blueprint(views, url_prefix='/')   #blueprints imported from views
    webApp.register_blueprint(authBP, url_prefix='/')    #blueprints imported from auth
    with webApp.app_context(): #An application context is created
        appDataBase.create_all()    #database tables created

    loginController = LoginManager()  #login manager set up
    loginController.login_view = 'auth.login' #auth.login set as the view
    loginController.init_app(webApp) #Flask login initialized
    @loginController.user_loader  #loading user based on ID
    def load_user(id):  #user loader function
        return User.query.get(int(id))  #loading user from database based on the ID

    return webApp  #returns flask app instance

def create_database(app):   #creates database for the given app, if it does not exist
    if not path.exists('website/' + DATABASE_NAME): # checks to see if database path does not exist
        appDataBase.create_all(app=app) #database created
