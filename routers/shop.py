from flask import Blueprint, render_template

shop = Blueprint('shop', __name__, url_prefix='/shop')

@shop.route('/')
def shop_home():
    # Pass products from your database here
    return render_template('shop.html')
