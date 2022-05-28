from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app=Flask(__name__)
app.config['SECRET_KEY'] = '1677626b7f3074acc0f04c9fdf6s145a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app) 
bcrypt=Bcrypt(app)
Login_manager=LoginManager(app)
Login_manager.login_view='login'
Login_manager.login_message_category='info'

from FlaskBlog import routes
