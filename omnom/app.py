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
""" This file contains the main app creator """
import os
import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
from omnom.recipe_db import RecipeDB, RecipeEntry
from omnom.recipe_view import bp as recipe_bp
from omnom.auth_view import bp as auth_bp
from werkzeug.security import generate_password_hash


def create_app(test_config=None):
    """ Return new flask app """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'omnom.sqlite'),
            )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.teardown_appcontext
    def close_db(exception):
        db = getattr(g, '_database', None)
        if db:
            db.close()

    app.register_blueprint(recipe_bp)
    app.register_blueprint(auth_bp)
    app.add_url_rule('/', endpoint='index')
    app.cli.add_command(init_db_command)

    return app


@click.command('init-db')
@with_appcontext
def init_db_command(extra_sql=None):
    """ Clear the existing data and create new tables."""
    rdb = RecipeDB(current_app.config['DATABASE'])
    rdb.init_db()
    add_user_sql = 'INSERT INTO user (username, password) VALUES (?, ?)'
    args = (username, generate_password_hash(password))
    if True:
        # FIXME: this preloads some recipes into the db - should remove at later stage of dev
        rdb.add_type('Pasta')
        rdb.add_type('Grains')
        rdb.add_type('Salads')
        rdb.add_type('Baked Goods')
        rdb.add_recipe(RecipeEntry(None, 'Mac Cheese', 'A tasty dish', 1))
        rdb.add_recipe(RecipeEntry(None, 'Blueberry Muffins', 'A breakfast food', 1))
        rdb.add_recipe(RecipeEntry(None, 'Caesar Salad', 'Eat all kings', 3))
        rdb.add_recipe(RecipeEntry(None, 'Fried Rice', 'A great way to use up leftovers', 2))
    click.echo('Initialized the database.')


if __name__ == '__main__':
    app = create_app()
    app.run()
