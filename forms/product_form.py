from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, IntegerField, SelectField, MultipleFileField, BooleanField,SubmitField
from wtforms.validators import DataRequired, NumberRange
from utils.enums import ProductCategory
from utils.utils import validate_phone

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    images = MultipleFileField('Product Images',id="add-product-images-field",description="Allows File Uploads")
    category = SelectField('Category', choices=[(cat.name, cat.value) for cat in ProductCategory], validators=[DataRequired()])
    description = TextAreaField('Description')
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    is_featured = BooleanField('Feature this product?')
    
    


class CheckoutForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Shipping Address", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired(),validate_phone])
    submit = SubmitField("Place Order")
    
class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)],id="rating-field")
    review_text = TextAreaField('Review',id="review-text")
    submit = SubmitField('Submit Review')

