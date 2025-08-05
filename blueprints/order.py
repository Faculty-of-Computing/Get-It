from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from models.order import Order
from core.database import db
from core.configs import logger

blueprint = Blueprint('order', __name__, url_prefix='/orders')

@blueprint.route('/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order:Order = Order.query.filter_by(id=order_id, user_id=current_user.id).first() # type: ignore
    if not order:
        abort(404)

    if request.method == 'POST':
        order.shipping_address = request.form.get('shipping_address', order.shipping_address)
        order.status = request.form.get('status', order.status) # type: ignore
        db.session.commit()
        logger.info('Order edited succesfuly')
        flash("Order updated successfully.", "success")
        return redirect(url_for('order.view_order', order_id=order.id))

    return render_template('order/edit_order.html', order=order)

@blueprint.route('/<int:order_id>')
@login_required
def view_order(order_id):
    # Fetch the order and ensure it belongs to the current user
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()

    if not order:
        abort(404)

    return render_template('order/view_order.html', order=order)
