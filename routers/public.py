from flask import Blueprint, render_template


router = Blueprint('about', __name__, url_prefix='/public')

@router.route('/')
def about_page():
    return render_template('about.html')

@router.route('/')
def privacy_page():
    return render_template('privacy.html')

@router.route('/')
def terms_page():
    return render_template('terms.html')

@router.route('/')
def faq_page():
    return render_template('faq.html')


@router.route('/')
def contact_page():
    return render_template('contact.html')