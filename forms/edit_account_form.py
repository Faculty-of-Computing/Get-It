from flask_wtf import FlaskForm
from h11 import Data
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class EditAccountForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField("Update")
