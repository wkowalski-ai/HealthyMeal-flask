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
        current_user.preferences = form.preferences.data
        db.session.commit()
        flash('Preferencje zostały zapisane.', 'success')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form, user=current_user)
