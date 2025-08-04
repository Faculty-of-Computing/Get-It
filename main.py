from flask import Flask, render_template, redirect, url_for, request, session
import os
from core.configs import  DATABASE_URL,BASE_DIR,DEBUG,SECRET_KEY,bycrypt
from core.database import db
from routers import auth,public,shop,cart,account
from core.configs import logger
from models import users,products
from services.auth import login_manager



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
    with app.app_context():
        db.create_all()
        logger.info("Models migrated")
    return app

app = create_app()




#NOTE - Routers are registered here
app.register_blueprint(auth.router) # type: ignore
app.register_blueprint(public.router)
app.register_blueprint(shop.router)
app.register_blueprint(cart.router)
app.register_blueprint(account.router)

@app.route('/') # type: ignore
def home():
   return render_template('index.html')



        
if __name__ == '__main__':
    app.run(debug=DEBUG,port=8000)






