from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Recipe

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
@login_required
def recipe_list():
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.updated_at.desc()).all()
    return render_template('recipe/index.html', recipes=recipes)
