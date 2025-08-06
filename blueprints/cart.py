from flask import Blueprint, session, redirect, url_for, render_template,  flash
from models.products import Products
from flask_login import login_required, current_user
from core.database import db
from models.order import Order, OrderItem
from core.configs import logger
from services.cart import get_cart
from models.cart import Cart,CartItem


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
    flash("Item added to cart",'success')
    return redirect(url_for('cart.view_cart'))


@blueprint.route('/remove/<int:product_id>', methods=['POST', 'GET'])
@login_required
def remove_from_cart(product_id):
    cart = current_user.cart
    if not cart:
        flash("No cart found",'info')
        return redirect(url_for('cart.view_cart'))

    item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        logger.info(f"{product_id} removed from cart")
        flash("Item removed from cart",'info')
    else:
        logger.info("item nnot in cart")
        flash("Item not in cart",'info')

    return redirect(url_for('cart.view_cart'))


