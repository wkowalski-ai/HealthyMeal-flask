from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from . import db

# Example route
from flask import Blueprint
main = Blueprint('main', __name__)

from flask_login import current_user

@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('welcome.html')
    return render_template('recipe/index.html')
