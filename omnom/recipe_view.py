#    Copyright 2021 Abigail Schubert
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" Recipe views such as index and full recipe page """
from flask import Blueprint, render_template, request, redirect, url_for, flash
from omnom.common import get_recipe_db, login_required
from omnom.recipe_db import RecipeEntry


bp = Blueprint('recipes', __name__)

class UserInputError(Exception):
    """ Exception related to bad user input """
    pass


@bp.route('/')
def index():
    """ Index page showing list of recipes """
    db = get_recipe_db()
    recipes = db.get_all_recipes()
    return render_template('recipes/index.html', recipes=recipes)


@bp.route('/recipes/<int:recipe_id>')
def full_recipe(recipe_id):
    """ Page showing full recipe info """
    db = get_recipe_db()
    recipe = db.get_recipe(recipe_id)
    return render_template('recipes/full_recipe.html', recipe=recipe)


def render_recipe_editor(recipe_id=None):
    """
    Render recipe editor page. If recipe_id is supplied, uses that recipe to
    populate form (edit recipe), otherwise form is blank (new recipe)
    """
    db = get_recipe_db()
    if recipe_id is None:
        recipe = RecipeEntry(id=-1, name='', description='', type_id=-1)
    else:
        recipe = db.get_recipe(recipe_id)
    food_types = db.get_all_types()
    return render_template('recipes/edit_recipe.html', recipe=recipe, food_types=food_types)


def validate_and_post_changes(recipe_id=None):
    """ Post changes to recipe, returns recipe_id """
    db = get_recipe_db()
    recipe = RecipeEntry(id=recipe_id,
                         name=request.form['name'],
                         description=request.form['description'],
                         type_id=request.form['food_type'])
    if not recipe.name:
        raise UserInputError('Recipe name is required.')
    elif not db.get_food_type(recipe.type_id):
        raise UserInputError('Unknown food category.')
    if recipe_id is None:
        recipe_id = db.add_recipe(recipe)
    else:
        db.update_recipe(recipe)
    return recipe_id


@bp.route('/recipes/create', methods=('GET', 'POST'))
@login_required
def create():
    """ Page showing new recipe editor """
    if request.method == 'POST':
        try:
            recipe_id = validate_and_post_changes()
        except UserInputError as error:
            flash(str(error))
        else:
            return redirect(url_for('recipes.full_recipe', recipe_id=recipe_id))
    return render_recipe_editor()


@bp.route('/recipes/<int:recipe_id>/edit', methods=('GET', 'POST'))
@login_required
def edit(recipe_id):
    """ Page showing recipe editor """
    if request.method == 'POST':
        try:
            recipe_id = validate_and_post_changes(recipe_id)
        except UserInputError as error:
            flash(str(error))
        else:
            return redirect(url_for('recipes.full_recipe', recipe_id=recipe_id))
    return render_recipe_editor(recipe_id)


@bp.route('/recipes/<int:recipe_id>/delete', methods=('POST',))
@login_required
def delete(recipe_id):
    """ POST: delete recipe from database """
    db = get_recipe_db()
    db.delete_recipe(recipe_id)
    return redirect(url_for('recipes.index'))
