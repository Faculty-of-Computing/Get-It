from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from forms.seller_application_form import SellerApplicationForm
from core.database import db
from models.users import User
from models.products import Products
from core.mail_config import MAIL_DEFAULT_SENDER

blueprint = Blueprint('seller', __name__, url_prefix='/seller')

@blueprint.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    form = SellerApplicationForm()
    if form.validate_on_submit():
        current_user.seller_application_status = 'pending'
        current_user.business_name = form.business_name.data
        current_user.business_description = form.business_description.data
        db.session.commit()
        flash('Your application has been submitted and is pending review.', 'info')
        return redirect(url_for('account.account'))
    return render_template('seller/apply.html', form=form, status=current_user.seller_application_status)

@blueprint.route('/applications')
@login_required
def applications():
    # Only admins can view all applications
    if not getattr(current_user, 'is_admin', False):
        flash('Unauthorized', 'danger')
        return redirect(url_for('account.account'))
    applicants = User.query.filter(User.seller_application_status != 'none').all()
    return render_template('admin/seller_applications.html', applicants=applicants)

@blueprint.route('/review/<int:user_id>/<string:action>', methods=['POST'])
@login_required
def review(user_id, action):
    # Only admins can approve/deny
    if not getattr(current_user, 'is_admin', False):
        flash('Unauthorized', 'danger')
        return redirect(url_for('account.account'))
    user = User.query.get_or_404(user_id)
    from core.configs import logger
    from flask_mail import Message
    from flask import current_app
    mail = getattr(current_app, 'mail', None)
    if action == 'approve':
        user.seller_application_status = 'approved'
        user.is_seller = True
        flash('Seller application approved.', 'success')
        logger.info(f"Admin {current_user.id} approved seller application for user {user.id}")
        if mail:
            msg = Message('Seller Application Approved', recipients=[user.email], sender=MAIL_DEFAULT_SENDER)
            msg.body = 'Congratulations! Your seller application has been approved.'
            mail.send(msg)
    elif action == 'deny':
        user.seller_application_status = 'denied'
        user.is_seller = False
        flash('Seller application denied.', 'info')
        logger.info(f"Admin {current_user.id} denied seller application for user {user.id}")
        if mail:
            msg = Message('Seller Application Denied', recipients=[user.email], sender=MAIL_DEFAULT_SENDER)
            msg.body = 'We regret to inform you that your seller application has been denied.'
            mail.send(msg)
    db.session.commit()
    return redirect(url_for('seller.applications'))

@blueprint.route('/<int:seller_id>')
def profile(seller_id):
    seller = User.query.get_or_404(seller_id)
    if not seller.is_seller:
        return "Not a seller", 404
    products = Products.query.filter_by(seller_id=seller.id).all()
    return render_template('seller/seller_profile.html', seller=seller, products=products)
