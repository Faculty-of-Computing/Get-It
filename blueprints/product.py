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

@blueprint.route('/category/<string:category>') # type: ignore
def category(category):
    categories = list(ProductCategory)
    # selected_category = next((cat for cat in categories if cat.name == category), None)
    products = get_products_by_category(category)
    return render_template('category/category.html', categories=categories, category_name=category, products=products)



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