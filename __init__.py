from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail



app=Flask(__name__)
app.config['SECRET_KEY'] = '1677626b7f3074acc0f04c9fdf6s145a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# s=URLSafeTimedSerializer(app.config['SECRET_KEY'])
db=SQLAlchemy(app) 
bcrypt=Bcrypt(app)
Login_manager=LoginManager(app)
Login_manager.login_view='users.login'
Login_manager.login_message_category='info'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='suajraika5sr@gmail.com'
app.config['MAIL_PASSWORD']='come15in3sonu2004'

mail=Mail(app)

from FlaskBlog.users.routes import users
from FlaskBlog.posts.routes import posts
from FlaskBlog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)