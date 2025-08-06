from flask import Blueprint, render_template, request, redirect, url_for, abort, flash,session
from flask_login import login_required, current_user
from models.order import Order,OrderItem
from core.database import db
from core.configs import logger,PAYSTACK_SECRET_KEY,PAYSTACK_PUBLIC_KEY
import requests as web_requests
from sqlalchemy.exc import SQLAlchemyError
from forms.product_form import CheckoutForm
import requests
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



@blueprint.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = current_user.cart
    if not cart or not cart.items:
        flash("Your cart is empty",'info')
        return redirect(url_for('cart.view_cart'))

    form = CheckoutForm()
    total_price = sum(item.product.price * item.quantity for item in cart.items)
    invalid_field = next((name for name, field in form._fields.items() if field.errors), None)

    if form.validate_on_submit():
        flash("Checkout details submitted successfully. Proceed to payment.", "success")
        # Save data in session for post-payment processing
        session['checkout_data'] = {
            'name': form.name.data.strip(), # type: ignore
            'address': form.address.data.strip(), # pyright: ignore[reportOptionalMemberAccess]
            'phone': form.phone.data.strip(), # type: ignore
            'total_price': total_price
        }
        return render_template('order/paystack_payment.html',
                               public_key=PAYSTACK_PUBLIC_KEY,
                               email=current_user.email,
                               amount=total_price * 100)  # Paystack uses kobo

    return render_template('cart/checkout.html', form=form, cart=cart, total=total_price,invalid_field=invalid_field)

@blueprint.route('/verify/<string:reference>')
@login_required
def verify_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
    response = requests.get(url, headers=headers).json()

    if response['status'] and response['data']['status'] == 'success':
        data = session.pop('checkout_data', None)
        if not data:
            flash("Session expired or missing checkout data.", "danger")
            return redirect(url_for('cart.view_cart'))

        try:
            # Create Order
            order = Order(
                user_id=current_user.id, # type: ignore
                shipping_address=data['address'], # type: ignore
                phone=data['phone'], # type: ignore
                total_price=data['total_price'], # type: ignore
                paystack_reference=reference # type: ignore
            )
            db.session.add(order)
            db.session.flush()

            # Add OrderItems
            for item in current_user.cart.items:
                db.session.add(OrderItem(
                    order_id=order.id, # type: ignore
                    product_id=item.product_id, # type: ignore
                    quantity=item.quantity, # type: ignore
                    price=item.product.price # type: ignore
                ))
                db.session.delete(item)

            db.session.commit()
            flash("Payment verified and order placed ✅", "success")
            return redirect(url_for('account.account'))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Order creation error: {e}")
            flash("Something went wrong while saving your order.", "danger")
            return redirect(url_for('cart.view_cart'))

    else:
        flash("Payment verification failed ❌", "danger")
        return redirect(url_for('cart.view_cart'))