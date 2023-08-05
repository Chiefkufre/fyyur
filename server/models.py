from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)
# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#


class Artists(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(
        db.String(500),
        nullable=True,
        default="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    )
    website_link = db.Column(db.String(50), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String(200), nullable=True, default="none")
    shows = db.relationship(
        "Show", backref="Artists", lazy=False, cascade="all, delete-orphan"
    )


class Venues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(200), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
    website = db.Column(db.String(120), nullable=True)
    seeking_description = db.Column(db.String(120), nullable=True)
    shows = db.relationship(
        "Show", backref="Venues", lazy=False, cascade="all, delete-orphan"
    )
    image_link = db.Column(
        db.String(500),
        nullable=True,
        default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    )
    facebook_link = db.Column(
        db.String(120), nullable=True, default="www.facebook.com/samuelkufrewillie"
    )


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id", ondelete="CASCADE"))
    start_time = db.Column(db.DateTime, nullable=False)
