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
""" Test config and fixtures """

import os
from pathlib import Path
import shutil
import tempfile
import pytest
from omnom.db import OmnomDB
from omnom.app import create_app

RESOURCES_DIR = Path(__file__).parent / 'resources'
TEST_SQL_FILE = RESOURCES_DIR / 'data.sql'


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    omnom_db = OmnomDB(db_path)
    omnom_db.init_db(extra_sql=TEST_SQL_FILE)

    app = create_app({'TESTING': True,
                      'DATABASE': db_path,
                      })

    source_image = RESOURCES_DIR / 'test.png'
    test_image = app.config['ASSETS_DIR'] / 'test.png'
    shutil.copy(source_image, test_image)

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    test_image.unlink(missing_ok=True)


class AuthActions():
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post('/auth/login',
                                 data={'username': username,
                                       'password': password})
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
