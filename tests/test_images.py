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
""" Unit tests for images.py """
import shutil
from conftest import RESOURCES_DIR
from omnom.images import save_to_assets, remove_asset


class FakeFileStorage:
    """ Mock of werkzeug FileStorage class """
    # pylint: disable=too-few-public-methods

    def __init__(self, src, filename):
        """
        Create a FakeFileStorage object.
        param src: full path to test file to provide
        param filename: filename of upload (doesn't need to be real)
        """
        self.src = src
        self.filename = filename

    def save(self, dest):
        """ Copy file to dest location """
        shutil.copy(self.src, dest)


def test_get_image(client):
    """ Verify that we can request images from assets directory. """
    response = client.get('/assets/test.png')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'


def test_remove_asset(client):
    """ Verify that we can remove images from assets directory. """
    response = client.get('/assets/test.png')
    assert response.status_code == 200
    remove_asset('test.png')
    response = client.get('/assets/test.png')
    assert response.status_code == 404


def test_save_to_assets(client):
    """ save_to_assets correctly stores file in assets dir """
    uploaded_file = FakeFileStorage(RESOURCES_DIR / 'test.png', 'foo.png')
    new_asset = save_to_assets(uploaded_file, 'mynewfile')
    assert new_asset.startswith('mynewfile')
    assert new_asset.endswith('.png')
    response = client.get('/assets/{}'.format(new_asset))
    assert response == 200
    assert response.mimetype == 'image/png'
