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
import logging
import os
import pathlib
import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from omnom.recipe_db import RecipeDB, RecipeEntry
from omnom.recipe_view import bp as recipe_bp
from omnom.user_db import UserDB
from omnom.auth_view import bp as auth_bp
from omnom.images import bp as images_bp


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def create_app(test_config=None):
    """ Return new flask app """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=pathlib.Path(app.instance_path, 'omnom.sqlite'),
            ASSETS_DIR=pathlib.Path(app.instance_path, 'assets'),
            )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    logger.info('Loaded app config: %s', app.config)

    for new_dir in [app.instance_path, app.config['ASSETS_DIR']]:
        new_dir = pathlib.Path(new_dir)
        new_dir.mkdir(parents=True, exist_ok=True)

    @app.teardown_appcontext
    def close_db(exception):
        db = getattr(g, '_database', None)
        if db:
            db.close()

    app.register_blueprint(recipe_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(images_bp)
    app.add_url_rule('/', endpoint='index')
    app.cli.add_command(init_db_command)
    logger.info('Created app')

    return app


@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables."""
    rdb = RecipeDB(current_app.config['DATABASE'])
    rdb.init_db()
    if True:
        # FIXME: this preloads some recipes into the db - should remove at later stage of dev
        rdb.add_type('Pasta')
        rdb.add_type('Grains')
        rdb.add_type('Salads')
        rdb.add_type('Baked Goods')
        rdb.add_recipe(RecipeEntry(name='Mac Cheese', description='A tasty dish', type_id=1))
        rdb.add_recipe(RecipeEntry(name='Blueberry Muffins', description='A breakfast food',
                                   type_id=4, ingredients='* Blueberries\n* Muffins',
                                   instructions='1. Mix blueberries and muffins\n1. Serve hot'))
        rdb.add_recipe(RecipeEntry(name='Caesar Salad', description='Eat all kings', type_id=3))
        rdb.add_recipe(RecipeEntry(name='Fried Rice', description='A great way to use up leftovers', type_id=2))
    udb = UserDB(current_app.config['DATABASE'])
    udb.add_user('admin', generate_password_hash('admin'))
    click.echo('Initialized the database.')


if __name__ == '__main__':
    app = create_app()
    app.run()
