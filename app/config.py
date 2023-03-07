from os import environ, path
from dotenv import load_dotenv
load_dotenv()

basedir = path.abspath(path.dirname(__file__))


class Config:

    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_APP = environ.get("FLASK_APP")
    TESTING = environ.get("TESTING")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIR = "./app/migrations"
