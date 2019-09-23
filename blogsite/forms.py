from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blogsite.models import User


class RegistrationForm(FlaskForm):
    username = StringField('User name', 
                            validators=[DataRequired(), Length(min=5, max=15)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])  
    password = PasswordField('Password',
                            validators=[DataRequired()])                                         
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up') 

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken,try another one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken,try another one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')                                                                
    submit = SubmitField('Login')                                                     