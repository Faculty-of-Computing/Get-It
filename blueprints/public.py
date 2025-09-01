from flask import Blueprint, render_template,flash,redirect,request,url_for
from utils.utils import allowed_file
import os
from werkzeug.utils import secure_filename


blueprint = Blueprint('public', __name__, url_prefix='/public')

@blueprint.route('/about')
def about():
    return render_template('public/about.html')

@blueprint.route('/privacy')
def privacy():
    return render_template('public/privacy.html')

@blueprint.route('/terms')
def terms():
    return render_template('public/terms.html')

@blueprint.route('/faq')
def faq():
    return render_template('public/faq.html')


@blueprint.route('/contact')
def contact():
    return render_template('public/contact.html')

