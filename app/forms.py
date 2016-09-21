from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

class UploadForm(Form):
    upload_file = FileField('File to Upload', validators=[DataRequired()])