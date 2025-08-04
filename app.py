from flask import Flask, render_template, redirect, url_for, request, session
import os
from core.configs import  DATABASE_URL,BASE_DIR,DEBUG
from core.database import db
from routers import auth
#from core.logger import logger

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'static'))

app.secret_key = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db.init_app(app)

#NOTE - Routters are registered here
app.register_blueprint(auth.router) # type: ignore

@app.route('/') # type: ignore
def home():
   return render_template('index.html')

@app.before_request
def on_startup():
    with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    app.run(debug=DEBUG,port=8000)






