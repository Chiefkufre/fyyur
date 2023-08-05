from flask import Flask, Response, flash, redirect, render_template, request, url_for
from flask_moment import Moment
from flask_wtf import FlaskForm, CSRFProtect

from .models import setup_db
from .views import views
from .config import DevConfig


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
def create_app_instance():
    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object(DevConfig)
    csrf = CSRFProtect(app)
   

     # registring app_context
    with app.app_context():
        setup_db(app)

    app.register_blueprint(views, url_prefix="/")

    if not app.debug:
        file_handler = FileHandler("error.log")
        file_handler.setFormatter(
            Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info("errors")

    return app
