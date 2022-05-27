from flask_wtf import FlaskForm    
from wtforms import StringField , EmailField ,PasswordField ,BooleanField , SubmitField 
from wtforms.validators import DataRequired , Length , Email , EqualTo



class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4) ,Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('Password',validators=[DataRequired(),Length(min=4) ,EqualTo('password') ])
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4) ,Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')	
