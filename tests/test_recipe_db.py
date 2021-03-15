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
""" Unit tests for the RecipeDB """
from pathlib import Path
import pytest
from omnom.recipe_db import RecipeEntry, RecipeDB


@pytest.fixture
def empty_db(tmp_path):
    """ A completely empty db with no recipes or food types """
    db_filename = Path(tmp_path) / 'foo.db'
    return RecipeDB(db_filename, init_db=True)


@pytest.fixture
def no_recipe_db(empty_db):
    """ Simple db with no recipes (but a couple food types) """
    rdb = empty_db
    rdb.add_type('Pasta')
    rdb.add_type('Grains')
    rdb.add_type('Salads')
    rdb.add_type('Baked Goods')
    return rdb

@pytest.fixture
def simple_db(no_recipe_db):
    """ Simple db with a few recipes and food types """
    rdb = no_recipe_db
    rdb.add_recipe(RecipeEntry(None, 'Mac Cheese', 'A tasty dish', 1))
    rdb.add_recipe(RecipeEntry(None, 'Blueberry Muffins', 'A breakfast food', 1))
    rdb.add_recipe(RecipeEntry(None, 'Caesar Salad', 'Eat all kings', 3))
    rdb.add_recipe(RecipeEntry(None, 'Fried Rice', 'A great way to use up leftovers', 2))
    return rdb


def test_init_db(empty_db):
    """ Test that init db initializes the db correctly. """
    db_cursor = empty_db.conn.cursor()
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    available_tables = map(tuple, db_cursor.fetchall())
    assert ('food_type',) in available_tables
    assert ('recipe',) in available_tables
    assert len(empty_db.get_all_types()) == 0


def test_add_food_type(empty_db):
    """ Test that adding food types works """
    empty_db.add_type('Pasta')
    empty_db.add_type('Breakfast')
    ret = empty_db.get_all_types()
    assert 'Pasta' in ret.values()
    assert 'Breakfast' in ret.values()


def test_get_type_id(simple_db):
    """ Test that getting the type_id from the food type str works """
    all_types = simple_db.get_all_types()
    type_id = simple_db.get_type_id('Pasta')
    assert all_types[type_id] == 'Pasta'
    type_id = simple_db.get_type_id('Rocks')
    assert type_id is None


def test_get_food_type(simple_db):
    """ Test that getting food type from the id# works """
    assert simple_db.get_food_type(1) == 'Pasta'
    assert simple_db.get_food_type(2) == 'Grains'


def test_get_missing_food_type(simple_db):
    """ Test that requesting a missing food type returns 'None' """
    assert simple_db.get_food_type(5000) == 'None'


def test_add_recipe(no_recipe_db):
    """ Test that we can add (and retrieve) a single recipe """
    rdb = no_recipe_db
    expected_name = 'Mac Cheese'
    expected_desc = 'A tasty dish'
    expected_type = 3
    new_recipe = RecipeEntry(None, expected_name, expected_desc, expected_type)
    rdb.add_recipe(new_recipe)
    all_recipes = rdb.get_all_recipes()
    assert len(all_recipes) == 1
    stored_recipe = all_recipes[0]
    assert stored_recipe.name == expected_name
    assert stored_recipe.description == expected_desc
    assert stored_recipe.type_id == expected_type


def test_add_multiple_recipes(no_recipe_db):
    """ Test that we can add (and retrieve) multiple recipes """
    rdb = no_recipe_db
    expected_recipes = [ RecipeEntry(None, '0', 'foo', 3),
                         RecipeEntry(None, '1', 'bar', 3),
                         RecipeEntry(None, '2', 'bar', 3),
                       ]
    for recipe in expected_recipes:
        rdb.add_recipe(recipe)
    all_recipes = rdb.get_all_recipes()
    assert len(all_recipes) == len(expected_recipes)
    found_names = [False,] * len(expected_recipes)
    for recipe in all_recipes:
        found_names[int(recipe.name)] = True
    assert all(found_names)


def test_get_recipe(simple_db):
    """ Test that we get the correct recipe when requesting by id. """
    rdb = simple_db
    ret = rdb.get_recipe(2)
    assert ret is not None
    assert ret.name == 'Blueberry Muffins'


def test_get_missing_recipe(simple_db):
    """ Test that we get None when recipe id does not exist. """
    rdb = simple_db
    ret = rdb.get_recipe(5000)
    assert ret is None
