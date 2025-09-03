from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Create Task')


class TaskStatusForm(FlaskForm):
    status = SelectField('Status', choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('done', 'Done')])
    submit = SubmitField('Update')


class TaskDeleteForm(FlaskForm):
    task_id = HiddenField()
    submit = SubmitField('Delete')
