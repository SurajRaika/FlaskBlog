import os 
class Config:
        
    SECRET_KEY = '1677626b7f3074acc0f04c9fdf6s145a'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('db_user_id')
    MAIL_PASSWORD=os.environ.get('db_user_password')
