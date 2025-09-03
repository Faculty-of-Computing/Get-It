from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required,current_user
from forms.product_form import AddProductForm,ReviewForm
from core.configs import logger,ALLOWED_EXTENSIONS
from utils.enums import ProductCategory
from services.product import add_new_product,get_products_by_category
from sqlalchemy import or_
from models.products import Products,Review
from core.database import db


blueprint = Blueprint('product', __name__,url_prefix='/product')


@blueprint.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        logger.debug("Proccessing request")
        try:
            logger.debug(form.images.data)
            add_new_product(form)
            logger.debug("Product addition finished")
            flash('Product added successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as err:
            flash(f'An error occured\n{err}','error')
            logger.info(err)
            return redirect(request.url)
    return render_template('products/add_product.html', form=form)

@blueprint.route('/category/<string:category>')
def category(category):
    categories = list(ProductCategory)
    # Get filter/sort params
    brand = request.args.get('brand')
    color = request.args.get('color')
    size = request.args.get('size')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    sort = request.args.get('sort')

    # Get all products in category
    products_query = Products.query.filter(Products.category == category)

    # Filtering
    if price_min is not None:
        products_query = products_query.filter(Products.price >= price_min)
    if price_max is not None:
        products_query = products_query.filter(Products.price <= price_max)

    # Sorting
    if sort == 'price_asc':
        products_query = products_query.order_by(Products.price.asc())
    elif sort == 'price_desc':
        products_query = products_query.order_by(Products.price.desc())
    elif sort == 'newest':
        products_query = products_query.order_by(Products.created_at.desc())
    elif sort == 'best_rated':
        products_query = products_query.order_by(Products.average_rating.desc())

    products = products_query.all()

    # For filter options, get distinct values from products in category
    all_products = Products.query.filter(Products.category == category).all()
    brands = sorted({getattr(p, 'brand', None) for p in all_products if getattr(p, 'brand', None)}) # type: ignore
    colors = sorted({getattr(p, 'color', None) for p in all_products if getattr(p, 'color', None)}) # type: ignore
    sizes = sorted({getattr(p, 'size', None) for p in all_products if getattr(p, 'size', None)}) #type: ignore

    return render_template(
        'category/category.html',
        categories=categories,
        category_name=category,
        products=products,
        brands=brands,
        colors=colors,
        sizes=sizes
    )



@blueprint.route('/search')
def search():
    query = request.args.get('search', '')
    # Ensure the query is not empty before searching
    if not query.strip():
        flash('Please enter a search term', 'info')
        return redirect(url_for('home'))

    search_query = f"%{query}%"
    logger.info(search_query)
    products = Products.query.filter( # type: ignore
        or_(
            Products.name.ilike(search_query),
            Products.description.ilike(search_query)
        )
    ).all()

    return render_template('products/search_result.html', products=products, query=query)



@blueprint.post('/<int:product_id>/review')
@login_required
def add_review(product_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            product_id=product_id, # type: ignore
            user_id=current_user.id, # type: ignore
            rating=form.rating.data, # type: ignore
            review_text=form.review_text.data # type: ignore
        ) # type: ignore
        db.session.add(review)
        db.session.commit()
        flash('Your review has been submitted.', 'success')
    else:
        flash('There was an error with your review.', 'danger')
    return redirect(url_for('product.product_detail', product_id=product_id))

@blueprint.route('/<int:product_id>')
def product_detail(product_id):
    product = Products.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).all()
    categories = list(ProductCategory)
    return render_template('products/product_detail.html', product=product, reviews=reviews, categories=categories)