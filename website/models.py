from . import dataBase
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(dataBase.Model):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    text = dataBase.Column(dataBase.String(10000))
    date = dataBase.Column(dataBase.DateTime(timezone=True), default=func.now())
    user_id = dataBase.Column(dataBase.Integer, dataBase.ForeignKey('user.id'))


class User(dataBase.Model, UserMixin):
    id = dataBase.Column(dataBase.Integer, primary_key=True)
    email = dataBase.Column(dataBase.String(150), unique=True)
    password = dataBase.Column(dataBase.String(150))
    first_name = dataBase.Column(dataBase.String(150))
    notes = dataBase.relationship('Note')
