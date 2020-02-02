from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask import current_app
from wtforms import SubmitField, SelectField, IntegerField, HiddenField
from wtforms_alchemy import ModelForm
from wtforms.validators import InputRequired, NumberRange
import re

from ..models import Event, photos
from ..models import Registration, EventStatus



class RegistrationForm(ModelForm, FlaskForm):
    class Meta:
        model = Registration
        exclude = ['status', 'level']

    user_id = IntegerField('Id')
    submit = SubmitField('Inscrire')


class EventForm(ModelForm, FlaskForm):
    class Meta:
        model = Event
        exclude = ['photo']
    photo_file = FileField(validators=[FileAllowed(photos, 'Image only!')])
    duplicate_photo = HiddenField()
    type = SelectField('Type', choices=[], coerce=int)


    def __init__(self, activity_choices, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.type.choices = activity_choices

    def set_default_description(self):
        description = current_app.config['DESCRIPTION_TEMPLATE']
        # Remove placeholders
        self.description.data = re.sub(r'\$[\w]+?\$', '', description)
