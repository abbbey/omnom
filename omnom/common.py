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
""" This file contains helpful common functions """
from flask import g, current_app
from omnom.recipe_db import RecipeDB
from omnom.user_db import UserDB


def get_recipe_db():
    """ Get reference to RecipeDB """
    db = getattr(g, '_database', None)
    if not db:
        db = g._database = RecipeDB(current_app.config['DATABASE'])
    return db

def get_user_db():
    """ Get a reference to UserDB """
    db = getattr(g, '_userdb', None)
    if not db:
        db = g._userdb = UserDB(current_app.config['DATABASE'])
    return db
