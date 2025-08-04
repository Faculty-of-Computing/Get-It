from flask import Blueprint, render_template

account = Blueprint('account', __name__, url_prefix='/account')

@account.route('/')
def account_page():
    # Pass user info from session/db here
    return render_template('account.html')
