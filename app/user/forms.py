# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class BookmarkForm(FlaskForm):
	href = StringField('href', validators=[DataRequired()])
	submit = SubmitField('Submit')