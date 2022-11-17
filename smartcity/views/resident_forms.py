from wtforms.validators import DataRequired, Length, InputRequired
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FileField


class NewTicket(FlaskForm):
    name = StringField("Name", [DataRequired()])
    description = TextAreaField("Description",
                                validators=[InputRequired(message="Please, tell us more about the problem"),
                                            Length(max=2048, message="Description is too long"),
                                            Length(min=20, message="Description is too short")])
    image = StringField("Image", [])
    reporter_id = IntegerField("Reporter_id", [DataRequired()])
