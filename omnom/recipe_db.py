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
import logging
from pathlib import Path
import sqlite3

logger = logging.getLogger(__name__)


class RecipeEntry():
    """ A RecipeEntry, comprised of name, description, and type_id"""

    def __init__(self, recipe_id, name, description, type_id):
        self.id = recipe_id
        self.name = name
        self.description = description
        self.type_id = type_id
        self.photo = ''

    @classmethod
    def from_db_row(cls, row):
        """ Create RecipeEntry from recipe db row. """
        new_recipe = RecipeEntry(recipe_id=row['id'],
                                 name=row['name'],
                                 description=row['description'],
                                 type_id=row['type_id'])
        new_recipe.photo = row['photo']
        return new_recipe


class RecipeDB():
    """ Interface to the database for storing recipes """

    SCHEMA_FILENAME = Path(__file__).parent / 'schema.sql'
    NONE_FOOD_TYPE = 'None'

    def __init__(self, db_filename, init_db=False):
        """ Connect to sqlite db located at db_filename """
        self.conn = sqlite3.connect(db_filename)
        self.conn.row_factory = sqlite3.Row
        logging.debug('Connected to %s', db_filename)
        if init_db:
            self.init_db()

    def __del__(self):
        self.close()

    def close(self):
        """ Close connection to db """
        if self.conn:
            self.conn.close()
            self.conn = None

    def _db_query(self, sql, args=None):
        """ Execute a SQL query. Returns a cursor with results. """
        cursor = self.conn.cursor()
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        return cursor

    def _db_insert(self, sql, args):
        """ Execute SQL insert statement and commit. """
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        self.conn.commit()

    def init_db(self):
        """ Reset and initialize database from empty """
        with open(self.SCHEMA_FILENAME) as fptr:
            cursor = self.conn.cursor()
            cursor.executescript(fptr.read())
        logging.info('Initialized recipe db using %s', self.SCHEMA_FILENAME)

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
        for key,value in ret:
            food_types[key] = value
        return food_types

    def add_recipe(self, recipe):
        """ Add a recipe to the database """
        food_type_id = self.get_type_id(recipe.type_id)
        self._db_insert('INSERT INTO recipe (name, description, type_id) VALUES (?,?,?)',
                        (recipe.name, recipe.description, recipe.type_id))
        return

    def get_recipe(self, recipe_id):
        """ Get recipe given recipe_id# """
        cursor = self._db_query('SELECT * from recipe WHERE id=?', (recipe_id,))
        ret = cursor.fetchone()
        if ret is None:
            return None
        else:
            return RecipeEntry.from_db_row(ret)

    def get_all_recipes(self):
        """ Get all recipes from the db """
        query = ('SELECT r.id, name, description, r.type_id, author_id, username'
             ' FROM post p JOIN user u ON p.author_id = u.id'
             ' WHERE p.id = ?')
        recipes = []
        cursor = self._db_query('SELECT * from recipe')
        for recipe_row in cursor.fetchall():
            print(tuple(recipe_row))
            recipe = RecipeEntry.from_db_row(recipe_row)
            recipes.append(recipe)
        return recipes

