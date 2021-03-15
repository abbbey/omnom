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
from flask import Blueprint, g, render_template
from omnom.common import get_db


bp = Blueprint('recipes', __name__)


@bp.route('/')
def index():
    """ Index page showing list of recipes """
    db = get_db()
    recipes = db.get_all_recipes()
    return render_template('recipes/index.html', recipes=recipes)


@bp.route('/recipes/<int:recipe_id>')
def full_recipe(recipe_id):
    """ Page showing full recipe info """
    db = get_db()
    recipe = db.get_recipe(recipe_id)
    return render_template('recipes/full_recipe.html', recipe=recipe)
