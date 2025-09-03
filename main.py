from flask import Flask, render_template, redirect, url_for

import os
from core.configs import  (DATABASE_URL,
                           DEBUG,
                           SECRET_KEY,
                           bycrypt,
                           CLOUDINARY_API_KEY,
                           CLOUDINARY_API_SECRET,
                           CLOUDINARY_NAME,
                           CLOUDINARY_URL)
from core.database import db
from blueprints import account, auth,public,cart,product,order as order_bp,admin
from core.configs import logger
from models import users,products,cart as cart_model,order
from models.products import Products
from services.auth import login_manager
from utils.enums import ProductCategory
import json
from typing import List
from flask_login import logout_user,current_user
import cloudinary
from datetime import datetime
import datetime as dt
from forms.product_form import ReviewForm
from flask_dance.contrib.google import make_google_blueprint, google



def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db.init_app(app)
    logger.info("Application started")
    login_manager.init_app(app)
    logger.info("Flask Login Loaded")
    login_manager.login_view = 'auth.login'  # type: ignore
    bycrypt.init_app(app)
    logger.info("App Binded to Bcrypt ")
    with app.app_context():
        db.create_all()
        logger.info("Models migrated")
    return app

app = create_app()

cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)


# Set up Google OAuth
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
google_bp = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=["profile", "email"],
    redirect_url="/google_login/callback"
)
app.register_blueprint(google_bp, url_prefix="/google_login")


#NOTE - blueprints are registered here
app.register_blueprint(auth.blueprint) 
app.register_blueprint(public.blueprint)
app.register_blueprint(cart.blueprint)
app.register_blueprint(account.blueprint)
app.register_blueprint(product.blueprint)
app.register_blueprint(order_bp.blueprint)
app.register_blueprint(admin.admin_bp)

@app.route('/')  # type: ignore
def home():
    categories = list(ProductCategory)  # If using Enum for categories
    #products = Products.query.limit(8).all()  # Load featured products (limit to 8 for performance/UI)
    products:List[Products] = db.session.execute(db.select(Products)).scalars().all() # type: ignore
    form = ReviewForm()
                
    return render_template('index.html', categories=categories, products=products, form=form)


#NOTE - created a global variable which is current_year that is injected into the Copyright section
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now(dt.timezone.utc).year}

#NOTE - RRuns before every request to ensure the user is logged in and is an active user
@app.before_request
def ensure_user_active():
    if current_user.is_authenticated and not current_user.is_active:
        logout_user()
        return redirect(url_for('auth.login'))

#NOTE - Creates a global tamplate function that is callable to return image urls based on category
@app.template_global('get_category_image_url')
def get_category_image_url(category_enum_value):
    """
    Returns the hard-coded Cloudinary URL for a given product category.
    This is a simple, direct mapping.
    """
    image_map = {
        ProductCategory.ELECTRONICS.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756291040/electronics.jpg",
        ProductCategory.CLOTHING.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756291041/clothing.jpg",
        ProductCategory.HOME_APPLIANCES.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756294159/home_appliances.jpg",
        ProductCategory.BOOKS.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756291032/books.jpg",
        ProductCategory.GROCERY.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756291040/grocery.jpg",
        ProductCategory.SPORTS.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756294299/sports.jpg",
        ProductCategory.TOYS.value:"https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756294300/toys.jpg",
        ProductCategory.BEAUTY.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756291031/beauty.jpg",
        ProductCategory.AUTOMOTIVE.value: "https://res.cloudinary.com/dpcqv1vjh/image/upload/v1756290937/automotive.jpg",
    }

    #NOTE Return the URL for the given category, or a default placeholder image if not found
    
    return image_map.get(category_enum_value, None)

if __name__ == '__main__':
    app.run(debug=DEBUG,host ='0.0.0.0', port=8000)






