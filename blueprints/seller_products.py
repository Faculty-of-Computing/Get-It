from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models.products import Products
from forms.product_form import AddProductForm
from core.database import db
import cloudinary.uploader

blueprint = Blueprint('seller_products', __name__, url_prefix='/seller/products')

@blueprint.route('/')
@login_required
def list_products():
    if not current_user.is_seller:
        abort(403)
    products = Products.query.filter_by(owner_id=current_user.id).all()
    return render_template('seller/my_products.html', products=products)

@blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_seller:
        abort(403)
    form = AddProductForm()
    if form.validate_on_submit():
        images = []
        if form.images.data:
            for image in form.images.data:
                upload_result = cloudinary.uploader.upload(image)
                images.append(upload_result['secure_url'])
        product = Products(
            name=form.name.data, # type: ignore
            price=form.price.data, # type: ignore
            description=form.description.data, # type: ignore
            stock=form.stock.data, # type: ignore
            category=form.category.data, # type: ignore
            images=images, # type: ignore
            owner_id=current_user.id # type: ignore
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added!', 'success')
        return redirect(url_for('seller_products.list_products'))
    return render_template('seller/add_product.html', form=form)

@blueprint.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Products.query.get_or_404(product_id)
    if not current_user.is_admin and product.owner_id != current_user.id:
        abort(403)
    form = AddProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated!', 'success')
        return redirect(url_for('seller_products.list_products'))
    return render_template('seller/edit_product.html', form=form, product=product)

@blueprint.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    if not current_user.is_admin and product.owner_id != current_user.id:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted!', 'info')
    return redirect(url_for('seller_products.list_products'))
