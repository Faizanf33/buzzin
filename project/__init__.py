import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

from project.exceptions import handle_exception
# get credentials from .env file
load_dotenv()

# instantiate the extensions
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__, static_url_path='')
    app.logger.setLevel(logging.INFO)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    from project.api import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from project.api import user_blueprint
    app.register_blueprint(user_blueprint)
    from project.api import article_blueprint
    app.register_blueprint(article_blueprint)

    @app.errorhandler(Exception)
    def manage_exception(ex):
        return handle_exception(ex)

    @app.errorhandler(404)
    def page_not_found(ex):
        return handle_exception(ex)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})

    return app
