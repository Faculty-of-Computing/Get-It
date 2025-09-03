from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    session,
    flash)
from services.user import register_user
from models.users import User
from sqlalchemy.exc import IntegrityError
from core.configs import logger,bycrypt
from forms.loginform import LoginForm
from flask_login import login_user,logout_user,login_required
from flask import request, redirect, url_for, render_template, flash, abort
from services.auth import url_has_allowed_host_and_scheme
from flask_dance.contrib.google import google
from core.database import db
from flask_dance.contrib.google import make_google_blueprint, google
from core.configs import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET


blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user:User = User.query.filter_by(username=form.username.data).first() # type: ignore

        if user and bycrypt.check_password_hash(user.password, form.password.data):
            logger.info("User authenticated succesfully")
            login_user(user)
            flash('Logged in successfully',"success")
            
            next_url = request.args.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.host):
                return redirect(next_url)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password','error')

    return render_template('account/login.html', form=form)


@blueprint.route('/signup', methods=['GET', 'POST']) # type: ignore
def register():
    error = None
    if request.method == 'POST':
        new_user = User(**request.form.to_dict())
        try:
            register_user(new_user)
            logger.info("Redirecting to auth/login")
            flash('Registration Successful','success')
            return redirect(url_for('auth.login'))
        except IntegrityError as e:
            logger.error(f"An error occurred {e}")
            flash("User already exists please try a different mail or username",'error')
            return render_template('account/register.html',)
        except Exception as e:
            flash(e.__str__(),'error')
            return render_template('account/register.html')
    return render_template('account/register.html')

@blueprint.post('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

# Set up Google OAuth
google_bp = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID, 
    client_secret=GOOGLE_CLIENT_SECRET, 
    scope=["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
    redirect_url="callback" 
)

@google_bp.route('/google/callback')
def google_callback():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    if not resp.ok:
        flash('Failed to fetch user info from Google.', 'error')
        return redirect(url_for('auth.login'))
    info = resp.json()
    email = info['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            username=info.get('name', email), # type: ignore
            email=email, # type: ignore
            first_name=info.get('given_name', ''), # type: ignore
            last_name=info.get('family_name', ''), # type: ignore
            profile_image=info.get('picture', None), # type: ignore
            is_active=True # type: ignore
        )
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash('Logged in with Google!', 'success')
    return redirect(url_for('account.account'))
