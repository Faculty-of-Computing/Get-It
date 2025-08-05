from flask import Blueprint, render_template

blueprint = Blueprint('account', __name__, url_prefix='/account')

@blueprint.route('/')
def account():
    # Pass user info from session/db here
    return render_template('account.html')
