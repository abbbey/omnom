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
""" This file contains the recipe db connections """
import json
import logging
import attr
from omnom.db import OmnomDB

logger = logging.getLogger(__name__)


@attr.s(kw_only=True)
class RecipeEntry():
    """ A RecipeEntry, comprised of name, description, and type_id"""
    # pylint: disable=too-few-public-methods

    id = attr.ib(default=None)  # pylint: disable=invalid-name
    name = attr.ib()
    description = attr.ib()
    type_id = attr.ib(default=-1)
    photo = attr.ib(default=None)
    ingredients = attr.ib(factory=list)
    instructions = attr.ib(factory=list)

    @classmethod
    def from_dict(cls, recipe_dict):
        """ Create RecipeEntry from recipe db row. """
        new_recipe = RecipeEntry(id=recipe_dict['id'],
                                 name=recipe_dict['name'],
                                 description=recipe_dict['description'],
                                 type_id=recipe_dict['type_id'],
                                 photo=recipe_dict['photo'])
        if 'ingredients' in recipe_dict.keys():
            new_recipe.ingredients = cls.deserialize(recipe_dict['ingredients'])
        if 'instructions' in recipe_dict.keys():
            new_recipe.instructions = cls.deserialize(recipe_dict['instructions'])
        return new_recipe

    @staticmethod
    def deserialize(input_str):
        """ Deserialize json into list, catching None """
        if input_str is None:
            return list()
        return json.loads(input_str)


class RecipeDB(OmnomDB):
    """ Interface to the database for storing recipes """

    NONE_FOOD_TYPE = 'None'

    def __init__(self, db_filename, init_db=False):
        """ Connect to sqlite db located at db_filename """
        super().__init__(db_filename=db_filename, init_db=init_db)

    def add_type(self, food_type):
        """ Add a food type to the database. """
        self._db_insert('INSERT INTO food_type (food_type) VALUES (?)', (food_type,))
        logging.debug('Added %s into food_type table', food_type)

    def get_type_id(self, food_type):
        """ Get food type given name. """
        cursor = self._db_query('SELECT id from food_type WHERE food_type=?', (food_type,))
        ret = cursor.fetchone()
        if ret is None:
            return ret
        return ret[0]

    def get_food_type(self, type_id):
        """ Get food type given id# """
        cursor = self._db_query('SELECT food_type from food_type WHERE id=?', (type_id,))
        ret = cursor.fetchone()
        if ret is None:
            return self.NONE_FOOD_TYPE
        return ret[0]

    def get_all_types(self):
        """ Return dict of food types """
        cursor = self._db_query('SELECT * from food_type')
        ret = cursor.fetchall()
        food_types = {}
        for row in ret:
            food_types[row['id']] = row['food_type']
        return food_types

    def add_recipe(self, recipe):
        """ Add a recipe to the database """
        sql = ('INSERT INTO recipe (name, description, type_id, ingredients, instructions, photo) '
               'VALUES (?,?,?,?,?,?)')
        ingredients = json.dumps(recipe.ingredients)
        instructions = json.dumps(recipe.instructions)
        recipe_id = self._db_insert(sql, (recipe.name, recipe.description, recipe.type_id,
                                          ingredients, instructions, recipe.photo))
        return recipe_id

    def get_recipe(self, recipe_id):
        """ Get full recipe given recipe_id# """
        cursor = self._db_query('SELECT * from recipe WHERE id=?', (recipe_id,))
        ret = cursor.fetchone()
        if ret is None:
            return None
        return RecipeEntry.from_dict(ret)

    def update_recipe(self, recipe):
        """ Update recipe in db """
        sql = ('UPDATE recipe SET name=?, description=?, type_id=?, ingredients=?, '
               'instructions=?, photo=? WHERE id=?')
        self._db_insert(sql, (recipe.name, recipe.description, recipe.type_id,
                              json.dumps(recipe.ingredients), json.dumps(recipe.instructions),
                              recipe.photo, recipe.id))

    def delete_recipe(self, recipe_id):
        """ Delete recipe from database """
        self.conn.execute('DELETE FROM recipe WHERE id = ?', (recipe_id,))
        self.conn.commit()

    def get_all_recipes(self):
        """ Get all recipes from the db """
        recipes = []
        cursor = self._db_query('SELECT id, name, description, type_id, photo from recipe')
        for recipe_row in cursor.fetchall():
            recipe = RecipeEntry.from_dict(recipe_row)
            recipes.append(recipe)
        return recipes
