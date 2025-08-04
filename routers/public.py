from flask import Blueprint, render_template


router = Blueprint('public', __name__, url_prefix='/public')

@router.route('/')
def about():
    return render_template('about.html')

@router.route('/')
def privacy():
    return render_template('privacy.html')

@router.route('/')
def terms():
    return render_template('terms.html')

@router.route('/')
def faq():
    return render_template('faq.html')


@router.route('/')
def contact():
    return render_template('contact.html')