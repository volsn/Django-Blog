from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea


class LeaveComment(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    text = TextField('Write a response...', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Publish')


class EditCommentForm(FlaskForm):
    text = TextField('Edit', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Save')


class LeaveReplyForm(FlaskForm):
    text = TextField('Reply', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Save')
