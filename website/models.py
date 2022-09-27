from dataclasses import dataclass
from . import db 
from sqlalchemy import create_engine
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.inspection import inspect
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
    # order = db.relationship("Order")

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

class Orders(db.Model):
    __tablename__='orders'
    id = db.Column(db.Integer,primary_key = True)
    reference = db.Column(db.String(5))
    status = db.Column(db.String(20))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.Integer)
    email = db.Column(db.String(50))
    pick_up_time = db.Column(db.String(20))
    card_number = db.Column(db.String(50))
    card_exp = db.Column(db.String(10))
    card_secure_code = db.Column(db.String(10))
    payment_type = db.Column(db.String(10))
    items = db.relationship('OrderDetail', backref='orders', lazy=True)
        
class OrderDetail(db.Model):
    __tablename__='orderdetail'
    id = db.Column(db.Integer,primary_key = True)
    ItemId = db.Column(db.Integer, db.ForeignKey("menu.id"))
    OrderId = db.Column(db.Integer, db.ForeignKey("orders.id"))
    qty = db.Column(db.Integer)
# DB_NAME = "database.db"
# engine = create_engine(url=f'sqlite:///{DB_NAME}')
# print(f'this is a new engine: {engine}')

# connection1 = engine.connect()
# print(connection1)
  
# table_name = 'Order'
  
# query = f'{table_name};'
# connection1.execute(query)

# inspect_tb = inspect(Order)
# for c in inspect_tb.c:
#     print(c.name)
