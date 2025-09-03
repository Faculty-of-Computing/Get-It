from flask import Blueprint, render_template,abort,redirect,url_for,flash
from flask_login import login_required,current_user
from models.order import Order
from forms.edit_account_form import EditAccountForm
from core.database import db
from flask import Blueprint, render_template
from flask_login import login_required
from utils.utils import admin_required
import cloudinary.uploader

blueprint = Blueprint('account', __name__, url_prefix='/account')

@blueprint.route('/')
@login_required
def account():
    # Fetch user orders from the database
    user_orders = (
        Order.query
        .filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    # user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.date.desc()).all()
    
    return render_template('account/account.html',orders=user_orders)


@blueprint.route("/edit", methods=["GET", "POST"])
@login_required
def edit_account():
    form = EditAccountForm(obj=current_user)

    if form.validate_on_submit():
        if form.profile_image.data:
            # Delete old image from Cloudinary if exists
            if current_user.profile_image:
                try:
                    public_id_with_extension = current_user.profile_image.split('/')[-1]
                    public_id = public_id_with_extension.rsplit('.', 1)[0]
                    cloudinary.uploader.destroy(public_id)
                except Exception as e:
                    flash(f"Error deleting old profile image: {e}", "error")
            # Upload new image
            upload_result = cloudinary.uploader.upload(form.profile_image.data)
            current_user.profile_image = upload_result['secure_url']
        if form.password.data:
            current_user.password = form.password.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        db.session.refresh(current_user)
        flash("Account updated successfully.", "success")
        return redirect(url_for("account.account"))

    return render_template("account/edit_account.html", form=form)

@blueprint.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Fetch data for the dashboard
    return render_template('admin/dashboard.html')
