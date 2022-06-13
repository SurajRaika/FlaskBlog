from flask import current_app
from FlaskBlog import db , Login_manager 

from itsdangerous import URLSafeTimedSerializer as Serializer
import datetime 
from flask_login import UserMixin



@Login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key=True)
    password=db.Column(db.String(60),nullable = False)
    email=db.Column(db.String(120),unique=True,nullable = False)
    image_file=db.Column(db.String(20),nullable = False, default='default.jpg')
    username=db.Column(db.String(20),nullable = False)

    posts = db.relationship('Post',backref ='author',lazy=True)
 
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"
    def get_token(self):
        serial=Serializer(current_app.config['SECRET_KEY'])
        return serial.dumps({'user_id':self.id})

    @staticmethod
    def varify_token(token, exipres_sec=300):
        serial=Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id=serial.loads(token,max_age=exipres_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)
            
class Post(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.datetime.utcnow)
    content = db.Column(db.Text , nullable=False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"




