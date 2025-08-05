from typing import List, Sequence
from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from models.products import Products
from flask_login import login_required, current_user
from core.database import db
from models.order import Order, OrderItem
from core.configs import logger
from services.cart import get_cart
from models.cart import Cart,CartItem
from sqlalchemy.exc import SQLAlchemyError
from forms.product_form import CheckoutForm

blueprint = Blueprint('cart', __name__, url_prefix='/cart')



@blueprint.route('/')
@login_required
def view_cart():
    # Get current user's cart
    cart = current_user.cart  # assuming one-to-one relationship

    if not cart or not cart.items:
        return render_template('cart/cart.html', cart_items=[], total=0)

    cart_items = []
    total = 0

    for item in cart.items:
        product = item.product
        if product:
            subtotal = product.price * item.quantity
            total += subtotal
            cart_items.append({
                'product': product,
                'quantity': item.quantity,
                'subtotal': subtotal
            })

    return render_template('cart/cart.html', cart_items=cart_items, total=total)


@blueprint.route('/add/<int:product_id>', methods=['POST', 'GET'])
@login_required
def add_to_cart(product_id):
    product = Products.query.get_or_404(product_id)

    # Get or create cart
    cart = current_user.cart
    if not cart:
        cart = Cart(user_id=current_user.id) # type: ignore
        db.session.add(cart)
        db.session.flush()

    # Check if item already exists
    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, user_id=current_user.id, quantity=1) # type: ignore
        db.session.add(item)

    db.session.commit()
    logger.info("Item added to cart")
    flash("Item added to cart.")
    return redirect(url_for('cart.view_cart'))


@blueprint.route('/remove/<int:product_id>', methods=['POST', 'GET'])
@login_required
def remove_from_cart(product_id):
    cart = current_user.cart
    if not cart:
        flash("No cart found.")
        return redirect(url_for('cart.view_cart'))

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        logger.info(f"{product_id} removed from cart")
        flash("Item removed from cart.")
    else:
        logger.info("item nnot in cart")
        flash("Item not in cart.")

    return redirect(url_for('cart.view_cart'))


@blueprint.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = current_user.cart
    if not cart or not cart.items:
        flash("Your cart is empty.")
        return redirect(url_for('cart.view_cart'))

    form = CheckoutForm()
    total_price = sum(item.product.price * item.quantity for item in cart.items)

    if form.validate_on_submit():
        try:
            # Create order
            order = Order(user_id=current_user.id, # type: ignore
                total_price=total_price, # type: ignore
                shipping_address=form.address.data.strip(), # type: ignore
                phone = form.phone.data.strip() # type: ignore
                )
            db.session.add(order)
            db.session.flush()  # so we get the order.id before committing

            # Add order items
            for item in cart.items:
                db.session.add(OrderItem(
                    order_id=order.id, # type: ignore
                    product_id=item.product_id, # type: ignore
                    quantity=item.quantity, # type: ignore
                    price=item.product.price # type: ignore
                ))

            # Clear cart items
            for item in cart.items:
                db.session.delete(item)

            db.session.commit()
            logger.info(f"Order #{order.id} placed by {current_user.username}")
            flash("Order placed successfully!")
            return redirect(url_for('account.account'))

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Checkout error: {e}")
            flash("Something went wrong. Please try again.")

    return render_template('cart/checkout.html', form=form, cart=cart, total=total_price)