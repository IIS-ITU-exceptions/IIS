from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField

from smartcity.models import User, RolesUsers


class NewTicket(FlaskForm):
    name = StringField("Name", [DataRequired()])
    description = TextAreaField("Description", [DataRequired(message="Please, tell us more about the problem"),
                                                Length(max=2048, message="Description is too long")])
    image = StringField("Image", [])
    reporter_id = IntegerField("Reporter_id", [DataRequired()])
