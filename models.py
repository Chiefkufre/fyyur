# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

from app import db

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class ArtistGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<Artist_Genre artist_id:{self.artist_id} genre: {self.genre}>"
    

  


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String, nullable=False, unique=True )
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=True)
    venues = db.relationship("Venue", secondary="shows", backref=db.backref("artists", lazy=True))
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String(), nullable=True, default="")
    genres = db.relationship("Artist_Genre", backref="artist", lazy=True)
    image_link = db.Column(
        db.String(500),
        nullable=True,
        default="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    )
   
    

class Show(db.Model):
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id", ondelete="CASCADE"), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    

class VenueGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venues.id", ondelete="CASCADE"), nullable=False )
    genre = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<Venue_Genre venue_id:{self.venue_id} genre: {self.genre}>"



class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True )
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.relationship("Venue_Genre", passive_deletes=True, backref="venue", lazy=True)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
    website = db.Column(db.String(120), nullable=True)
    seeking_description = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True,
        default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    )
    facebook_link = db.Column(db.String(120), nullable=True, default="www.facebook.com/samuelkufrewillie")
   

