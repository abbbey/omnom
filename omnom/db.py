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
""" Common access to omnom database """
import logging
from pathlib import Path
import sqlite3

logger = logging.getLogger(__name__)


class OmnomDB():
    """ Common access to the omnom db, used by RecipeDB and UserDB """

    SCHEMA_FILENAME = Path(__file__).parent / 'schema.sql'

    def __init__(self, db_filename, init_db=False):
        """ Connect to sqlite db located at db_filename """
        self.conn = sqlite3.connect(db_filename)
        self.conn.row_factory = sqlite3.Row
        logger.debug('Connected to %s', db_filename)
        if init_db:
            self.init_db()

    def __del__(self):
        self.close()

    def close(self):
        """ Close connection to db """
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_db(self, extra_sql=None):
        """ Reset and initialize database from empty """
        with open(self.SCHEMA_FILENAME) as fptr:
            cursor = self.conn.cursor()
            cursor.executescript(fptr.read())
        if extra_sql:
            with open(extra_sql) as fptr:
                cursor = self.conn.cursor()
                cursor.executescript(fptr.read())
        self.conn.commit()
        logger.info('Initialized recipe db using %s', self.SCHEMA_FILENAME)

    def _db_query(self, sql, args=None):
        """ Execute a SQL query. Returns a cursor with results. """
        cursor = self.conn.cursor()
        if args:
            if not isinstance(args, tuple):
                raise Exception("args isn't a tuple. Forgot to put a comma, didn't you?")
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        return cursor

    def _db_insert(self, sql, args):
        """ Execute SQL insert statement and commit. """
        if not isinstance(args, tuple):
            raise Exception("args isn't a tuple. Forgot to put a comma, didn't you?")
        cursor = self.conn.cursor()
        cursor.execute(sql, args)
        self.conn.commit()
