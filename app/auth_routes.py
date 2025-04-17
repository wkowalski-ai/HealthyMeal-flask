from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, ResetPasswordForm
from .models import User
from . import db
from .email import send_password_reset_email

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already registered.', 'danger')
            return redirect(url_for('auth.register'))
        new_user = User(email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Jeśli podany adres istnieje w naszej bazie, wysłaliśmy instrukcje resetowania hasła.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Nieprawidłowy lub wygasły token resetowania hasła.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Hasło zostało zresetowane. Możesz się teraz zalogować.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
