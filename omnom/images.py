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
""" This file contains methods for interacting with user-images """
from datetime import datetime
import logging
from pathlib import Path
from flask import Blueprint, current_app, send_from_directory
from werkzeug.utils import secure_filename


logger = logging.getLogger(__name__)  # pylint:disable=invalid-name
bp = Blueprint('images', __name__)  # pylint:disable=invalid-name

ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg'}


def save_to_assets(file_obj, prefix):
    """ Given file_obj, save to user assets directory and return filename """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    old_filename = secure_filename(file_obj.filename)
    file_ext = Path(old_filename).suffix
    new_filename = '{}_{}{}'.format(prefix, timestamp, file_ext)
    file_obj.save(current_app.config['ASSETS_DIR'] / new_filename)
    logger.info('Saved new asset %s', new_filename)
    return new_filename


def remove_asset(filename):
    """ Given filename, remove from user assets directory. """
    full_path = current_app.config['ASSETS_DIR'] / filename
    logger.info('Removing asset file %s', full_path)
    full_path.unlink(missing_ok=True)


@bp.route('/assets/<filename>')
def uploaded_file(filename):
    """ Returns file from user assets directory """
    return send_from_directory(current_app.config['ASSETS_DIR'], filename)
