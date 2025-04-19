from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import ProfileForm
from . import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.allergies = form.allergies.data
        current_user.excluded_products = form.excluded_products.data
        current_user.favorite_products = form.favorite_products.data
        db.session.commit()
        flash('Profil został zapisany.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form, user=current_user)
