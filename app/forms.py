from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, BooleanField, validators, PasswordField
from wtforms.validators import DataRequired

class UploadForm(Form):
    upload_file = FileField('File to Upload', [validators.DataRequired()])


class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class RegistrationForm(Form):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    #TODO add terms of service
