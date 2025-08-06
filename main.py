from flask import Flask, render_template, redirect, url_for
import os
from core.configs import  DATABASE_URL,BASE_DIR,DEBUG,SECRET_KEY,bycrypt
from core.database import db
from blueprints import account, auth,public,cart,product,order as order_bp
from core.configs import logger,UPLOAD_FOLDER
from models import users,products,cart as cart_model,order
from models.products import Products
from services.auth import login_manager
from utils.enums import ProductCategory
import json
from typing import List
from flask_login import logout_user,current_user

logger.info(f'Base Dir {BASE_DIR}')

def create_app():
    app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))
    app.secret_key = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    db.init_app(app)
    logger.info("Application started")
    login_manager.init_app(app)
    logger.info("Flask Login Loaded")
    login_manager.login_view = 'auth.login'  # type: ignore
    bycrypt.init_app(app)
    logger.info("App Binded to Bcrypt ")
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    with app.app_context():
        db.create_all()
        logger.info("Models migrated")
    return app

app = create_app()




#NOTE - blueprints are registered here
app.register_blueprint(auth.blueprint) # type: ignore
app.register_blueprint(public.blueprint)
app.register_blueprint(cart.blueprint)
app.register_blueprint(account.blueprint)
app.register_blueprint(product.blueprint)
app.register_blueprint(order_bp.blueprint)

@app.route('/')  # type: ignore
def home():
    categories = list(ProductCategory)  # If using Enum for categories
    #products = Products.query.limit(8).all()  # Load featured products (limit to 8 for performance/UI)
    products:List[Products] = db.session.execute(db.select(Products)).scalars().all() # type: ignore
    for product in products:
        if isinstance(product.images, str):
            try:
                product.images = json.loads(product.images)
                #logger.info(product.images)
            except json.JSONDecodeError:
                product.images = []
                
    return render_template('index.html', categories=categories, products=products)


@app.before_request
def ensure_user_active():
    if current_user.is_authenticated and not current_user.is_active:
        logout_user()
        return redirect(url_for('auth.login'))

        
if __name__ == '__main__':
    app.run(debug=DEBUG,port=8000)






