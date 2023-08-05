import os
from .settings import DB_NAME, DB_PASSWORD, DB_USER, DB_HOST, DB_PORT, DB_TYPE, SECRET_KEY


def create_db_url(DB_TYPE):
    if DB_TYPE == "postgresql":
        DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    elif DB_TYPE == "mysql":
        DATABASE_URI = f"mysql+{MYSQL_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    elif DB_TYPE == "sqlite":
        DATABASE_URI = "sqlite:///database.db"
    else:
        raise ValueError("Invalid DB_TYPE specified.")

    return DATABASE_URI


class DevConfig:
    """class to hold application configuration."""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True

    SECRET_KEY = SECRET_KEY

    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Enable debug mode.
    DEBUG = True

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = create_db_url(DB_TYPE)
    
    # "sqlite:///database.db"
    
    "postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"



