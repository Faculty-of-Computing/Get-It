from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from models.products import Products
from flask_login import login_required, current_user
from core.database import db
from models.order import Order, OrderItem
from core.configs import logger
blueprint = Blueprint('cart', __name__, url_prefix='/cart')


def get_cart():
    return session.get('cart', {})


def save_cart(cart):
    session['cart'] = cart
    session.modified = True


@blueprint.route('/')
def view_cart():
    cart = get_cart()
    product_ids = cart.keys()
    products = Products.query.filter(Products.id.in_(product_ids)).all()
    
    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})

    return render_template('cart/cart.html', cart_items=cart_items, total=total)


@blueprint.route('/add/<int:product_id>',methods=['POST','GET'])
def add_to_cart(product_id):
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    save_cart(cart)
    flash("Item added to cart.")
    return redirect(url_for('cart.view_cart'))


@blueprint.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = get_cart()
    if str(product_id) in cart:
        del cart[str(product_id)]
        save_cart(cart)
        flash("Item removed from cart.")
    return redirect(url_for('cart.view_cart'))


@blueprint.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = get_cart()
    if not cart:
        flash("Your cart is empty.")
        return redirect(url_for('cart.view_cart'))

    product_ids = cart.keys()
    products = Products.query.filter(Products.id.in_(product_ids)).all()

    total_price = sum(product.price * cart[str(product.id)] for product in products)

    if request.method == 'POST':
        shipping_address = request.form['shipping_address']

        order = Order(user_id=current_user.id, total_price=total_price, shipping_address=shipping_address) # type: ignore
        db.session.add(order)
        db.session.flush()  # Get order ID before commit

        for product in products:
            quantity = cart[str(product.id)]
            order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price) # type: ignore
            db.session.add(order_item)
            logger.info('Order created successfully')

        db.session.commit()
        session.pop('cart', None)
        flash("Order placed successfully!")
        return redirect(url_for('account.account'))

    return render_template('cart/checkout.html', total=total_price)

