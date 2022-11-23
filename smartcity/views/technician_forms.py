"""
File containing the forms for the technician views

@author: David Novák
@email: xnovak2r@stud.fit.vutbr.cz
"""


from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField


class UpdateServiceTask(FlaskForm):
    id = IntegerField("id")
    cost = IntegerField("cost", [DataRequired(message="Forgot to set cost?")])
    man_hours = IntegerField("man_hours", [DataRequired(message="Forgot calculate man-hours?")])
    completion = DateField("completion", [DataRequired(message="Forgot pass planned date of completion?")])
    # task_state = SelectField()
