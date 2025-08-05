from flask import Blueprint, render_template,flash,redirect,request,url_for
from utils.utils import allowed_file
import os
from werkzeug.utils import secure_filename
from core.configs import UPLOAD_FOLDER

blueprint = Blueprint('public', __name__, url_prefix='/public')

@blueprint.route('/')
def about():
    return render_template('about.html')

@blueprint.route('/')
def privacy():
    return render_template('privacy.html')

@blueprint.route('/')
def terms():
    return render_template('terms.html')

@blueprint.route('/')
def faq():
    return render_template('faq.html')


@blueprint.route('/')
def contact():
    return render_template('contact.html')

@blueprint.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No image part')
            return redirect(request.url)

        file = request.files['image']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # pyright: ignore[reportArgumentType]
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            flash('File uploaded successfully')
            return redirect(request.url)
        else:
            flash('Invalid file type')
            return redirect(request.url)

    return render_template('upload.html')