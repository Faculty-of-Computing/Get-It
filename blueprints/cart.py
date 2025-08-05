from flask import Blueprint, render_template

blueprint = Blueprint('cart', __name__, url_prefix='/cart')

@blueprint.route('/')
def cart():
    # Pass cart items from session/db here
    return render_template('cart.html')
