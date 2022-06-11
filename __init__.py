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
Login_manager.login_view='login'
Login_manager.login_message_category='info'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='surajraika5sr@gmail.com'
app.config['MAIL_PASSWORD']='YJA6hdnu2_iy5Tu'

mail=Mail(app)

from FlaskBlog import routes
