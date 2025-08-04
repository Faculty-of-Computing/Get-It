from flask import Blueprint, render_template

cart = Blueprint('cart', __name__, url_prefix='/cart')

@cart.route('/')
def cart_page():
    # Pass cart items from session/db here
    return render_template('cart.html')
