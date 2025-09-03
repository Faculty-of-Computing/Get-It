from flask_wtf import FlaskForm
# from h11 import Data
from wtforms import StringField, SubmitField, FileField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class EditAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    profile_image = FileField('Profile Image')
    password = PasswordField('New Password', validators=[
        Optional(),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm New Password')
    submit = SubmitField("Update")
