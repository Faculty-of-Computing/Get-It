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
router = Blueprint('user', __name__, url_prefix='/auth')

@router.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # user = users.get(username)
        # if user and user['password'] == password:
        #     session['username'] = username
        #     return redirect(url_for('home'))
        # else:
        #     error = 'Invalid username or password.'
    return render_template('login.html', error=error)

@router.route('/signup', methods=['GET', 'POST']) # type: ignore
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        new_user = User(**request.form.to_dict())
        try:
            register_user(new_user)
            return redirect(url_for('login'))
        except IntegrityError:
            flash("User already exists please try a different mail or username")
        except Exception as e:
            flash(e.__str__())
            return render_template('register.html', error=error)
    return render_template('register.html')