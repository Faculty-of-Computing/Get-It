from flask import Blueprint, jsonify, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models.wishlist import Wishlist
from models.products import Products
from core.database import db

blueprint = Blueprint('wishlist', __name__, url_prefix='/wishlist')

@blueprint.route('/')
@login_required
def view_wishlist():
    items = Wishlist.query.filter_by(user_id=current_user.id).all()
    products = [item.product for item in items]
    return render_template('account/wishlist.html', products=products)

@blueprint.route('/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    existing = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not existing:
        entry = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(entry)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Added to wishlist'})
    return jsonify({'success': False, 'message': 'Already in wishlist'})

@blueprint.route('/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    entry = Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Removed from wishlist'})
    return jsonify({'success': False, 'message': 'Not found in wishlist'})
