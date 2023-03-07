import os
from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config
from .models import User
from .utilities.db import bcrypt, db

migrate = Migrate(directory="./app/migrations")
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.secret_key = os.urandom(15)
    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    Bootstrap4(app)
    app.config["BOOTSTRAP_SERVE_LOCAL"] = True

    from app.errors.handlers import errors
    from app.main.routes import main
    from app.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)
    return app
