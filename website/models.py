from dataclasses import dataclass
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))




class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) # make sure same email not registered twice
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    notes = db.relationship("Note")

class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer,primary_key = True)
    item_name = db.Column(db.String(150),unique=True)
    item_name_cn = db.Column(db.String(150),unique=True)
    price = db.Column(db.Float)
    description = db.Column(db.String(150))
    image = db.Column(db.String(150))
    categoryID = db.Column(db.Integer, db.ForeignKey("menucategory.id"))

class MenuCategory(db.Model):
    __tablename__='menucategory'
    id = db.Column(db.Integer,primary_key = True)
    category = db.Column(db.String(150),unique=True)
    category_cn = db.Column(db.String(150),unique=True)


