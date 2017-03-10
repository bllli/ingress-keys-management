# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import Required, Length, Email, Regexp, DataRequired
from wtforms import ValidationError
from ..models import Role, User


class AddPortalForm(FlaskForm):
    name = StringField('po名', validators=[DataRequired(), Length(0, 128)])
    area = StringField('所处区域', validators=[Length(0,128)])
    link = StringField('PORTAL link', validators=[Length(0, 128)])
    submit = SubmitField('提交')
