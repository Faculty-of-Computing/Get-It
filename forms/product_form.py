from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, IntegerField, SelectField, MultipleFileField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from utils.enums import ProductCategory

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    images = MultipleFileField('Product Images')
    category = SelectField('Category', choices=[(cat.name, cat.value) for cat in ProductCategory], validators=[DataRequired()])
    description = TextAreaField('Description')
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    is_featured = BooleanField('Feature this product?')
