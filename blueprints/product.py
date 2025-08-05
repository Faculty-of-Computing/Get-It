from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
from models.products import Products
from core.database import db
from forms.product_form import AddProductForm
import os
from core.configs import logger,ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from utils.utils import allowed_file
from services.product import add_new_product


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
