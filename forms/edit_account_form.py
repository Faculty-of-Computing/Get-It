from flask_wtf import FlaskForm
# from h11 import Data
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Email

class EditAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    profile_image = FileField('Profile Image')
    submit = SubmitField("Update")
