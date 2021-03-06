"""Cowrie Frontend API for collecting log data."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

from flask_mongoengine import MongoEngine

from donthackme_api.events.views import events
from donthackme_api.admin.views import admin
from donthackme_api.users.views import users


DEFAULT_BLUEPRINTS = [
    events,
    admin,
    users
]


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""
    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_app(app):
    """Retrieve App Configuration."""
    app.config.from_object('donthackme_api.default_config')
    app.config.from_envvar('DONTHACKME_API_SETTINGS')
    print app.config.get("MONGODB_SETTINGS")


def configure_logging(app):
    """Add Rotating Handler to app."""
    logfile = app.config.get('LOG_FILE')
    handler = TimedRotatingFileHandler(
        logfile,
        when='h',
        interval=24,
        backupCount=30
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)


def create_app(app_name=None, blueprints=None):
    """Create the flask app."""
    if app_name is None:
        app_name = "cowrie_api"
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name)

    configure_app(app)
    configure_logging(app)

    db = MongoEngine()
    db.app = app
    db.init_app(app)

    configure_blueprints(app, blueprints)

    return app


if __name__ == "__main__":
    app = create_app(app_name=__name__)
    app.run(host="0.0.0.0", port=5000, debug=True)
