from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea


class GetInTouchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    company = StringField('Company')
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextField('Message', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Send')
