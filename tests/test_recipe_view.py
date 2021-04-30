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
from omnom.common import get_recipe_db


def test_index(client):
    """ Index page shows expected links and expected number of recipe entries """
    db = get_recipe_db()
    response = client.get('/')
    assert response.status_code == 200
    page = str(response.data, encoding='utf-8')
    assert '>Register</a>' in page
    assert '>Log In</a>' in page
    assert page.count('recipe-entry') == len(db.get_all_recipes())


def test_index_logged_in(client, auth):
    """ Index page when logged in shows username and logout links """
    auth.login('test', 'test')
    response = client.get('/')
    page = str(response.data, encoding='utf-8')
    assert 'test' in page
    assert '>Log Out</a>' in page
    assert 'New Recipe' in page


def test_full_recipe(client):
    """ Full recipe view shows full recipe info """
    response = client.get('/recipes/2')
    assert response.status_code == 200
    page = str(response.data, encoding='utf-8')
    assert 'Fried Rice' in page
    assert 'Edit' not in page
    assert 'Delete' not in page


def test_full_recipe_logged_in(client, auth):
    """ Full recipe view shows edit/delete links when logged in """
    auth.login('test', 'test')
    response = client.get('/recipes/2')
    page = str(response.data, encoding='utf-8')
    assert 'Edit' in page
    assert 'Delete' in page


def test_edit_recipe(client, auth):
    """ Recipe editor has expected controls """
    auth.login('test', 'test')
    response = client.get('/recipes/2/edit')
    page = str(response.data, encoding='utf-8')
    assert 'input name="name"' in page
    assert 'textarea name="description"' in page
    assert 'select name="food_type"' in page
    assert 'textarea name="ingredients"' in page
    assert 'textarea name="instructions"' in page
    food_types = get_recipe_db().get_all_types()
    for id_number, food_type in food_types.items():
        if id_number == 2:
            type_option = '<option value="{}" selected="selected">{}'.format(id_number, food_type)
        else:
            type_option = '<option value="{}">{}'.format(id_number, food_type)
        assert type_option in page

def test_edit_recipe_not_logged_in(client):
    """ Recipe editor redirects to login page if not logged in """
    response = client.get('/recipes/2/edit')
    assert response.headers['Location'] == 'http://localhost/auth/login'
