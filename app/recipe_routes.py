from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .models import Recipe
from . import db
from .forms import RecipeForm

recipe_bp = Blueprint('recipe', __name__)

from .forms import DeleteRecipeForm

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
@login_required
def recipe_list():
    recipes = Recipe.query.filter_by(user_id=current_user.id).order_by(Recipe.updated_at.desc()).all()
    delete_forms = {recipe.id: DeleteRecipeForm() for recipe in recipes}
    return render_template('recipe/index.html', recipes=recipes, delete_forms=delete_forms)

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
@login_required
def create_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipe(
            title=form.title.data,
            ingredients=form.ingredients.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()
        flash('Przepis został dodany!', 'success')
        return redirect(url_for('recipe.recipe_list'))
    return render_template('recipe/create_recipe.html', form=form)

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash('Brak dostępu do tego przepisu.', 'danger')
        return redirect(url_for('recipe.recipe_list'))
    db.session.delete(recipe)
    db.session.commit()
    flash(f'Przepis "{recipe.title}" został usunięty.', 'success')
    return redirect(url_for('recipe.recipe_list'))

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
        recipe.ingredients = form.ingredients.data
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
    preferences = current_user.preferences
    if not preferences or not preferences.strip():
        ai_result = None
        ai_error = "Aby skorzystać z funkcji AI, uzupełnij swoje preferencje żywieniowe w profilu użytkownika."
    else:
        api_key = current_app.config.get('OPENROUTER_API_KEY')
        ai_result, ai_error = modify_recipe_with_ai(recipe.content, preferences, api_key)
        if ai_error:
            # Zamień typowe błędy na czytelne komunikaty
            if "Brak klucza API" in ai_error:
                ai_error = "Brak klucza API do AI. Skontaktuj się z administratorem." 
            elif "Błąd API OpenRouter" in ai_error:
                ai_error = "Wystąpił problem z połączeniem z AI. Spróbuj ponownie później lub skontaktuj się z administratorem." 
            elif "Nie udało się uzyskać odpowiedzi" in ai_error:
                ai_error = "AI nie zwróciło odpowiedzi. Spróbuj ponownie później."
            elif "Błąd podczas komunikacji" in ai_error:
                ai_error = "Wystąpił błąd podczas komunikacji z AI. Spróbuj ponownie później."
    return render_template('recipe/ai_result.html', recipe=recipe, ai_result=ai_result, ai_error=ai_error)
