from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Create Thread')

class MessageForm(FlaskForm):
    body = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')
