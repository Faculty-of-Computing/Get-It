from flask import Blueprint, render_template

router = Blueprint('account', __name__, url_prefix='/account')

@router.route('/')
def account():
    # Pass user info from session/db here
    return render_template('account.html')
