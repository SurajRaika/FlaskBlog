from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt



app=Flask(__name__)
app.config['SECRET_KEY'] = '1677626b7f3074acc0f04c9fdf6s145a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app) 
bcrypt=Bcrypt(app)


from FlaskBlog import routes
