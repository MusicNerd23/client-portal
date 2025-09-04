from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional


class TicketForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('urgent', 'Urgent')])
    submit = SubmitField('Create Ticket')


class TicketStatusForm(FlaskForm):
    status = SelectField('Status', choices=[('new', 'New'), ('open', 'Open'), ('pending', 'Pending'), ('resolved', 'Resolved'), ('closed', 'Closed')])
    submit = SubmitField('Update')


class TicketCommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Comment')


class TicketAssignForm(FlaskForm):
    assignee = SelectField('Assign To', coerce=int)
    submit = SubmitField('Assign')
