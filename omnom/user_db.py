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
""" This file contains the user db connections """
import logging
from omnom.db import OmnomDB


logger = logging.getLogger(__name__)


class UserEntry():

    def __init__(self, id_number, name, password):
        self.id_number = id_number
        self.name = name
        self.password = password


class UserDB(OmnomDB):

    def __init__(self, db_filename, init_db=False):
        """ Connect to sqlite db located at db_filename """
        super().__init__(db_filename=db_filename, init_db=init_db)

    def get_user(self, id_number):
        """ Get UserEntry given id_number """
        cursor = self._db_query('SELECT * from user WHERE id=?', (id_number,))
        ret = cursor.fetchone()
        if ret is None:
            return None
        return UserEntry(ret['id'], ret['name'], ret['password'])

    def get_user_by_name(self, name):
        """ Get UserEntry given name """
        cursor = self._db_query('SELECT * from user WHERE name=?', (name,))
        ret = cursor.fetchone()
        if ret is None:
            return None
        return UserEntry(ret['id'], ret['name'], ret['password'])

    def add_user(self, name, password):
        """ Add new user to db """
        if self.get_user_by_name(name):
            raise Exception("User already exists")
        self._db_insert('INSERT INTO user (name, password) VALUES (?, ?)',
                        (name, password))
