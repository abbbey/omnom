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
import pytest
from flask import g, session
from omnom.common import get_user_db


def test_register(client, app):
    """ able to register a new user """
    assert client.get('/auth/register').status_code == 200
    response = client.post('/auth/register',
                           data={'username': 'a', 'password': 'a'})
    assert response.headers['Location'] == 'http://localhost/auth/login'

    with app.app_context():
        ret = get_user_db().get_user_by_name('a')
        assert ret is not None


@pytest.mark.parametrize(( 'username', 'password', 'message'),
                         ((''        , ''        , b'Username is required.'),
                          ('a'       , ''        , b'Password is required.'),
                          ('test'    , 'test'    , b'already registered'),
                          ))
def test_register_validate_input(client, username, password, message):
    """ register form catches common input errors """
    response = client.post('/auth/register',
                           data={'username': username, 'password': password})
    assert message in response.data


def test_login(client, auth):
    """ login sets uer_id in session variable """
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    client.get('/')
    assert session['user_id'] == 1
    assert g.user.name == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'),
                         (('a'       , 'test'    , b'Incorrect username.'),
                          ('test'    , 'a'       , b'Incorrect password.'),
                          ))
def test_login_validate_input(auth, username, password, message):
    """ login catches common input errors """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(auth):
    """ user_id is removed from session after logout """
    auth.login()
    auth.logout()
    assert 'user_id' not in session
