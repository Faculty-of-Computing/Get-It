from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from forms.product_form import AddProductForm
from core.configs import logger,ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from utils.enums import ProductCategory
from services.product import add_new_product,get_products_by_category


blueprint = Blueprint('product', __name__,url_prefix='/product')


@blueprint.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        try:
            add_new_product(form)
            flash('Product added successfully!', 'success')
            return redirect(url_for('product.add_product'))
        except Exception:
            flash('An error occured','error')
            return redirect(request.url)
    return render_template('products/add_product.html', form=form)

@blueprint.route('/category/<string:category>') # type: ignore
def category(category):
    categories = list(ProductCategory)
    products = get_products_by_category(category)
    return render_template('index.html', categories=categories, products=products)
