from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref


class Staff(UserMixin, db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False,
                      unique=True)  # create email column
    password = db.Column(db.String(100),
                         nullable=False)  # cerate password column


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    orders_rel = relationship('OrdersOngoing', back_populates='menu_rel')
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)


class OrdersOngoing(db.Model):
    __tablename__ = 'current_orders'
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    menu_rel = relationship('Menu', backref=backref("menu", uselist=False))
    name = db.Column(db.String, nullable=False)
    table = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)


class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    table = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=True)
    time = db.Column(db.String, nullable=True)
    orders_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
