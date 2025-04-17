from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import RegistrationForm
from .models import User
from . import db

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Sprawdź czy email nie jest zajęty (walidacja jest też w formularzu)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html', form=form)
        # Stwórz użytkownika
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
