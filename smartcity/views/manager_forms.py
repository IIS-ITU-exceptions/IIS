"""
File containing the forms for the manager views

@author: Ladislav Vašina
@email: xvasin11@stud.fit.vutbr.cz
"""

from wtforms.validators import Email, DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField

from smartcity.models import User, RolesUsers


class CreateTechnician(FlaskForm):
    name = StringField("Name", [DataRequired(message="Forgot technician name?")])
    surname = StringField("Surname", [DataRequired(message="Forgot technician surname?")])
    email = StringField("Email Address", [Email(), DataRequired(message="Forgot technician email address?")])
    password = PasswordField("Password", [
        DataRequired(message="You must provide a password."),
        Length(min=8, message="Password must be at least 8 characters long."),
        EqualTo("confirm", message="Passwords must match.")
    ])
    confirm = PasswordField("Repeat Password", [EqualTo("password", message="Passwords must match.")])


class CreateServiceTask(FlaskForm):
    name = StringField("Name", [DataRequired(message="Forgot service task name?")])
    description = TextAreaField("Description", [DataRequired(message="Forgot service task description?")])
