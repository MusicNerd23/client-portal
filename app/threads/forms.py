from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Optional

class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create Thread')

class MessageForm(FlaskForm):
    body = TextAreaField('Message', validators=[DataRequired()])
    attachment = FileField('Attachment', validators=[Optional()])
    submit = SubmitField('Send Message')
