# Import necessary modules
from . import appDataBase
from flask_login import UserMixin
from sqlalchemy.sql import func

# Define the Note model and its columns
class Note(appDataBase.Model):
    id = appDataBase.Column(appDataBase.Integer, primary_key=True)
    noteText = appDataBase.Column(appDataBase.String(5000))
    noteDate = appDataBase.Column(appDataBase.DateTime(timezone=True), default=func.now())
    userId = appDataBase.Column(appDataBase.Integer, appDataBase.ForeignKey('user.id'))

# Define the User model and its columns
class User(appDataBase.Model, UserMixin):
    id = appDataBase.Column(appDataBase.Integer, primary_key=True)
    eMail = appDataBase.Column(appDataBase.String(150), unique=True)
    password = appDataBase.Column(appDataBase.String(150))
    fName = appDataBase.Column(appDataBase.String(150))
    notes = appDataBase.relationship('Note')    # Define the relationship between User and Note models