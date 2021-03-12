
import pytest
from omnom.recipe_db import RecipeEntry, RecipeDB

@pytest.fixture
def empty_db(tmp_path):
    """ A completely empty db with no recipes or food types """
    return RecipeDB(tmp_path, init_db=True)

@pytest.fixture
def simple_db(empty_db):
    """ Simple db with no recipes (but a couple food types """
    rdb = empty_db
    rdb.add_type('Pasta')
    rdb.add_type('Grains')
    rdb.add_type('Salads')
    rdb.add_type('Baked Goods')
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

def test_add_recipe(simple_db):
    """ Test that we can add (and retrieve) a single recipe """
    expected_name = 'Mac Cheese'
    expected_desc = 'A tasty dish'
    expected_type = 3
    new_recipe = RecipeEntry(None, expected_name, expected_desc, expected_type)
    simple_db.add_recipe(new_recipe)
    all_recipes = simple_db.get_all_recipes()
    assert len(all_recipes) == 1
    stored_recipe = all_recipes[0]
    assert stored_recipe.name == expected_name
    assert stored_recipe.description == expected_desc
    assert stored_recipe.type_id == expected_type

def test_add_multiple_recipes(simple_db):
    """ Test that we can add (and retrieve) multiple recipes """
    expected_recipes = [ RecipeEntry(None, '0', 'foo', 3),
                         RecipeEntry(None, '1', 'bar', 3),
                         RecipeEntry(None, '2', 'bar', 3),
                       ]
    for recipe in expected_recipes:
        simple_db.add_recipe(recipe)
    all_recipes = simple_db.get_all_recipes()
    assert len(all_recipes) == len(expected_recipes)
    found_names = [False,] * len(expected_recipes)
    for recipe in all_recipes:
        found_names[int(recipe.name)] = True
    assert all(found_names)


