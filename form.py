from flask_wtf import FlaskForm
from wtforms import StringField , EmailField ,PasswordField ,BooleanField , SubmitField
from wtforms.validators import DataRequired , Length , Email , EqualTo



class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4,max=20) ,Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('Password',validators=[DataRequired(),Length(min=4) ,EqualTo('password') ])
    submit = SubmitField('Sign up')	


class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=5,max=20)])
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4,max=20) ,Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login Form')	
