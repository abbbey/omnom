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
""" auth.py provides endpoints related to login/authorization """
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from omnom.common import get_user_db
from omnom.user_db import UserDB


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """ GET:  provide registration form
        POST: validate input and create new user
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_db = get_user_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif user_db.get_user_by_name(username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user_db.add_user(username, generate_password_hash(password))
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """ GET:  provide user login page
        POST: authenticate user using username/password and begin user session
    """
    if request.method == 'POST':
        user_db = get_user_db()
        user_entry = user_db.get_user_by_name(request.form['username'])
        given_password = request.form['password']

        error = None
        if user_entry is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user_entry.password, given_password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user_entry.id_number
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """ End user session """
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    """ Update application context with current user. g.user will contain
    UserEntry for the current user, or None if no user is logged in.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_db().get_user(user_id)


def login_required(view):
    """ Wrap a view which requires login. Returns redirect to login page if
    no user is active.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view
    return render_template('auth/login.html')
