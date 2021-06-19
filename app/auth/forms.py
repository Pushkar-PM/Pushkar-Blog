from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length
from app.models import User
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username=StringField(_l('username'),validators=[DataRequired()])
    password=PasswordField(_l('password'),validators=[DataRequired()])
    remember_me=BooleanField(_l('remember_me'))
    submit=SubmitField(_l('Sign_In'))

class RegistrationForm(FlaskForm):
    username=StringField(_l('username'),validators=[DataRequired()])
    email=StringField(_l('email'),validators=[DataRequired(),Email()])
    password=PasswordField(_l('password'),validators=[DataRequired()])
    password2=PasswordField(_l('repeat password'),validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField(_l('Register'))

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_("Already used"))

    def validate_email(self,email):
        email=User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError(_("Use different"))
    

class ResetPasswordRequestForm(FlaskForm):
    email=StringField(_l('Email'),validators=[DataRequired(),Email()])
    submit=SubmitField(_l('Request reset'))

class ResetPasswordForm(FlaskForm):
    password=PasswordField(_l('password'),validators=[DataRequired()])
    password2=PasswordField(_l('confirm password'),validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField(_l('Reset'))