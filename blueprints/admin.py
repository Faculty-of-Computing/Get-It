from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.products import Products
from models.order import Order, OrderItem
from forms.product_form import AddProductForm
from core.database import db
import cloudinary.uploader
from utils.utils import admin_required
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates/admin')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    products = Products.query.all()
    
    # Sales trends (last 30 days)
    sales_trends_query = db.session.query(
        func.date(Order.created_at),
        func.count(Order.id)
    ).filter(Order.created_at >= datetime.now() - timedelta(days=30)).group_by(func.date(Order.created_at)).all()
    
    sales_trends_labels = [res[0].strftime('%b %d') for res in sales_trends_query] if sales_trends_query else []
    sales_trends_data = [res[1] for res in sales_trends_query] if sales_trends_query else []

    # Revenue (last 30 days)
    revenue_query = db.session.query(
        func.date(Order.created_at),
        func.sum(Order.total_price)
    ).filter(Order.created_at >= datetime.now() - timedelta(days=30)).group_by(func.date(Order.created_at)).all()

    revenue_labels = [res[0].strftime('%b %d') for res in revenue_query] if revenue_query else []
    revenue_data = [float(res[1]) for res in revenue_query] if revenue_query else []

    # Top selling products
    top_products_query = db.session.query(
        Products.name,
        func.sum(OrderItem.quantity)
    ).join(OrderItem, Products.id == OrderItem.product_id).group_by(Products.name).order_by(func.sum(OrderItem.quantity).desc()).limit(5).all()

    top_products_labels = [res[0] for res in top_products_query] if top_products_query else []
    top_products_data = [res[1] for res in top_products_query] if top_products_query else []

    return render_template(
        'dashboard.html', 
        products=products,
        sales_trends_labels=sales_trends_labels,
        sales_trends_data=sales_trends_data,
        revenue_labels=revenue_labels,
        revenue_data=revenue_data,
        top_products_labels=top_products_labels,
        top_products_data=top_products_data
    )

@admin_bp.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        images = []
        if form.images.data:
            for image in form.images.data:
                upload_result = cloudinary.uploader.upload(image)
                images.append(upload_result['secure_url'])
        new_product = Products(
            name=form.name.data,# type: ignore
            price=form.price.data,# type: ignore
            description=form.description.data,# type: ignore
            stock=form.stock.data,# type: ignore
            category=form.category.data,# type: ignore
            images=images #type :ignore # type: ignore
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_product.html', form=form)

@admin_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Products.query.get_or_404(product_id)
    form = AddProductForm(obj=product)
    existing_images = product.images if product.images else []
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(product)
        updated_images = []
        # For each existing image, check if a new file was uploaded for its slot
        for idx, old_image_url in enumerate(existing_images):
            file_field = f'image_{idx}'
            new_file = request.files.get(file_field)
            if new_file and new_file.filename:
                # Delete old image from Cloudinary
                try:
                    public_id_with_extension = old_image_url.split('/')[-1]
                    public_id = public_id_with_extension.rsplit('.', 1)[0]
                    cloudinary.uploader.destroy(public_id)
                except Exception as e:
                    flash(f"Error deleting old image {old_image_url}: {e}", "error")
                # Upload new image
                upload_result = cloudinary.uploader.upload(new_file)
                updated_images.append(upload_result['secure_url'])
            else:
                # Keep old image
                updated_images.append(old_image_url)
        # Handle any new images added beyond the original count
        extra_files = request.files.getlist('extra_images')
        for extra_file in extra_files:
            if extra_file and extra_file.filename:
                upload_result = cloudinary.uploader.upload(extra_file)
                updated_images.append(upload_result['secure_url'])
        product.images = updated_images
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/edit_product.html', form=form, product=product, existing_images=existing_images)

@admin_bp.route('/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)
    # Delete images from Cloudinary
    if product.images:
        for image_url in product.images:
            try:
                public_id_with_extension = image_url.split('/')[-1]
                public_id = public_id_with_extension.rsplit('.', 1)[0]
                cloudinary.uploader.destroy(public_id)
            except Exception as e:
                flash(f"Could not delete image {image_url} from Cloudinary: {e}", "error")
    db.session.delete(product)
    db.session.commit()
    flash('Product and associated images deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))
