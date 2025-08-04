from flask import Blueprint, render_template

router = Blueprint('cart', __name__, url_prefix='/cart')

@router.route('/')
def cart():
    # Pass cart items from session/db here
    return render_template('cart.html')
