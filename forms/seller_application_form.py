from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class SellerApplicationForm(FlaskForm):
    business_name = StringField('Business Name', validators=[DataRequired(), Length(max=100)])
    business_description = TextAreaField('Business Description', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Apply to Become a Seller')
