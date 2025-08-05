from flask import Blueprint, render_template
from flask_login import login_required
from models.or

blueprint = Blueprint('account', __name__, url_prefix='/account')

@blueprint.route('/')
@login_required
def account():
    # Fetch user orders from the database
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    
    return render_template('account.html', orders=user_orders)
