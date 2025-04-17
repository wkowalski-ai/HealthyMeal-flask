from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Recipe
from . import db
from .forms import RecipeForm

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
@login_required
def recipe_list():
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.updated_at.desc()).all()
    return render_template('recipe/index.html', recipes=recipes)

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
@login_required
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipe(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()
        flash('Przepis został dodany!', 'success')
        return redirect(url_for('recipe.recipe_list'))
    return render_template('recipe/create_recipe.html', form=form)

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('Brak dostępu do tego przepisu.', 'danger')
        return redirect(url_for('recipe.recipe_list'))
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.content = form.content.data
        db.session.commit()
        flash('Przepis został zaktualizowany!', 'success')
        return redirect(url_for('recipe.view_recipe', recipe_id=recipe.id))
    return render_template('recipe/edit_recipe.html', form=form, recipe=recipe)

@recipe_bp.route('/recipes/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('Brak dostępu do tego przepisu.', 'danger')
        return redirect(url_for('recipe.recipe_list'))
    return render_template('recipe/view_recipe.html', recipe=recipe)

@recipe_bp.route('/recipes/<int:recipe_id>/modify', methods=['POST'])
@login_required
def modify_recipe(recipe_id):
    from flask import current_app
    from .utils import modify_recipe_with_ai
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('Brak dostępu do tego przepisu.', 'danger')
        return redirect(url_for('recipe.recipe_list'))
    preferences = current_user.preferences or ""
    api_key = current_app.config.get('OPENROUTER_API_KEY')
    ai_result, ai_error = modify_recipe_with_ai(recipe.content, preferences, api_key)
    return render_template('recipe/ai_result.html', recipe=recipe, ai_result=ai_result, ai_error=ai_error)
