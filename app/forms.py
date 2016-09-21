from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField, BooleanField, validators
from wtforms.validators import DataRequired

class UploadForm(Form):
    upload_file = FileField('File to Upload', validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), validators.email()])
    password = StringField('Email', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)