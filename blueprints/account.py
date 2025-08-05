from flask import Blueprint, render_template,abort,redirect,url_for,flash
from flask_login import login_required,current_user
from models.order import Order
from forms.edit_account_form import EditAccountForm
from core.database import db
from flask import Blueprint, render_template
from flask_login import login_required
# from models.or

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
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data

        db.session.commit()
        flash("Account updated successfully.", "success")
        return redirect(url_for("account.account"))

    return render_template("account/edit_account.html", form=form)



    return render_template('account.html')