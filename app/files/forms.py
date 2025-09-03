from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class FileUploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')


class FileDeleteForm(FlaskForm):
    file_id = HiddenField()
    submit = SubmitField('Delete')
