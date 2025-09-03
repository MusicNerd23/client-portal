from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Optional


class OrgUserCreateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Optional()])
    role = SelectField('Role', choices=[('client', 'Client'), ('client_admin', 'Client Admin')])
    submit = SubmitField('Add User')


class OrgUserDeleteForm(FlaskForm):
    user_id = HiddenField()
    submit = SubmitField('Remove')

