from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# configure app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# configure database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL1",
                                                       "sqlite:///menu.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, session_options={"autoflush": False})

# import all files needed to initialize the app
from app import forms
from app import models
from app import menus
from app import admin