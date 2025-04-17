from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from . import db

# Example route
from flask import Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('recipe/index.html')
