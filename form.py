from flask_wtf import FlaskForm    
from wtforms import StringField , EmailField ,PasswordField ,BooleanField , SubmitField  , IntegerField
from wtforms.validators import DataRequired , Length , Email , EqualTo 



class RegistrationForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired(),Length(min=2,max=20)])
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4) ,Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    confirm_password=PasswordField('Password',validators=[DataRequired(),Length(min=4) ,EqualTo('password') ])
    submit = SubmitField('Sign Up')
class LoginForm(FlaskForm):
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4) ,Email()])
    password=PasswordField('Password',validators=[DataRequired(),Length(min=4)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')	
class AccountForm(FlaskForm):
    username=StringField('Name',validators=[DataRequired(),Length(min=2,max=20)])
    mobile_number=IntegerField("Mobile Number")
    email=EmailField('Email Address',validators=[DataRequired(),Length(min=4) ,Email()])
