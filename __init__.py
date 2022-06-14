
from venv import create
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from FlaskBlog.config import Config



# s=URLSafeTimedSerializer(app.config['SECRET_KEY'])
db=SQLAlchemy() 
bcrypt=Bcrypt()
Login_manager=LoginManager()
Login_manager.login_view='users.login'
Login_manager.login_message_category='info'


mail=Mail()


def create_app(config_class=Config):

    app=Flask(__name__)


    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    Login_manager.init_app(app)
    mail.init_app(app)



    from FlaskBlog.error.handlers import errors
    from FlaskBlog.users.routes import users
    from FlaskBlog.posts.routes import posts
    from FlaskBlog.main.routes import main

    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    
    return app