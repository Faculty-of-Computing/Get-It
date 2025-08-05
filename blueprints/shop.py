from flask import Blueprint, render_template

blueprint = Blueprint('shop', __name__, url_prefix='/shop')

@blueprint.route('/')
def shop():
    # Pass products from your database here
    return render_template('shop.html')
