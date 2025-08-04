from flask import Blueprint, render_template

router = Blueprint('shop', __name__, url_prefix='/shop')

@router.route('/')
def shop():
    # Pass products from your database here
    return render_template('shop.html')
