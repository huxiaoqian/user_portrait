# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.validators import DataRequired, Optional, Length
from wtforms import ValidationError
from wtforms import StringField


class SearchForm(Form):

    name = StringField('name', validators=[Optional()])
