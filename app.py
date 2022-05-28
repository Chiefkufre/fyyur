#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil
from dateutil.parser import parse
import babel
from datetime import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from models import db, Artists, Venues, Show
# from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
# db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)


# #----------------------------------------------------------------------------#
# # Models
# #----------------------------------------------------------------------------#

# class Artists(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True )
#     city = db.Column(db.String(120), nullable=False)
#     state = db.Column(db.String(120), nullable=False)
#     phone = db.Column(db.String(120), nullable=False)
#     genres = db.Column(db.ARRAY(db.String), nullable=False)
#     facebook_link = db.Column(db.String(120), nullable=True)
#     image_link = db.Column(db.String(500), nullable=True,
#         default="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
#     )
#     website_link = db.Column(db.String(50), nullable=True)
#     seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
#     seeking_description = db.Column(db.String(200), nullable=True, default="none")
#     shows = db.relationship("Show", backref="Artists", lazy=False, cascade="all, delete-orphan")
    
   
   
# class Venues(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String, nullable=False)
#   email = db.Column(db.String, nullable=False, unique=True )
#   city = db.Column(db.String(120), nullable=False)
#   state = db.Column(db.String(120), nullable=False)
#   address = db.Column(db.String(120), nullable=False)
#   phone = db.Column(db.String(120), nullable=True)
#   genres = db.Column(db.ARRAY(db.String)
#                      , nullable=False)
#   seeking_talent = db.Column(db.Boolean, nullable=True, default=False)
#   website = db.Column(db.String(120), nullable=True)
#   seeking_description = db.Column(db.String(120), nullable=True)
#   shows = db.relationship("Show", backref="Venues", lazy=False, cascade="all, delete-orphan")
#   image_link = db.Column(db.String(500), nullable=True,
#       default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
#   )
#   facebook_link = db.Column(db.String(120), nullable=True, default="www.facebook.com/samuelkufrewillie")
    

# class Show(db.Model):
#     artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), primary_key=True)
#     venue_id = db.Column(db.Integer, db.ForeignKey("venues.id", ondelete="CASCADE"), primary_key=True)
#     start_time = db.Column(db.DateTime, nullable=False)
    





#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []
  results = Venues.query.distinct(Venues.city, Venues.state).all()
  for result in results:
      city_and_state = {
          "city": result.city,
          "state": result.state
      }
      venues = Venues.query.filter_by(city=result.city, state=result.state).all()

      # format each venue
      formatted_venues = []
      for venue in venues:
          formatted_venues.append({
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(list(filter(lambda x: x.start_time > datetime.now(), venue.shows)))
          })
      
      city_and_state["venues"] = formatted_venues
      data.append(city_and_state)
  return render_template('pages/venues.html', areas=data);




@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  
  data = {}
  
  # querying the venue table
  venue_query = Venues.query.get(venue_id)
    
  # for past shows and events
  # events = Show.query.all()
  event_before_now = db.session.query(Show).join(Venues).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all() 
  # Show.query.filter(Show.start_time < datetime.now()).all()
  past_shows = []
  for event in  event_before_now:
    artist = Artists.query.get(event.artist_id)
    artist_data = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(event.start_time)
        } 
    past_shows.append(artist_data)
    
  # for upcoming shows and events
  new_upcoming_shows = db.session.query(Show).join(Venues).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()
  upcoming_shows = []
  for show in new_upcoming_shows:
    artist = Artists.query.get(show.artist_id)
    artist_data = {
              "artist_id": artist.id,
              "artist_name": artist.name,
              "artist_image_link": artist.image_link,
              "start_time": str(show.start_time)
          }
    upcoming_shows.append(artist_data)
   
  #  assigning values to thr data dictionary 
  data = {
  'id': venue_query.id,
  "name": venue_query.name,
  'genres': venue_query.genres.split(","),
  "address": venue_query.address,
  "city": venue_query.city,
  "state": venue_query.state,
  "phone": venue_query.phone,
  "website": venue_query.website,
  "facebook_link": venue_query.facebook_link,
  "seeking_talent": venue_query.seeking_talent,
  "seeking_description": venue_query.seeking_description,
  "image_link": venue_query.image_link,
  "past_shows": past_shows,
  "upcoming_shows": upcoming_shows,
  "past_shows_count": len(past_shows),
  "upcoming_shows_count": len(upcoming_shows)
}
 
  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm()
  # TODO: modify data to be the data object returned from db insertion
  venue = Venues.query.filter_by(email=form.email.data).first()
  if venue:
    flash(f'Sorry, a venue is is already listed with this email: {form.email.data}')
    return render_template('pages/home.html')
  elif form.validate_on_submit():
    fname = form.name.data.strip()
    femail = form.email.data
    fphone = form.phone.data.strip()
    fcity = form.city.data
    fstate = form.state.data
    faddress = form.address.data
    fwebsite = form.website_link.data
    fimage = form.image_link.data
    fgenres = form.genres.data                  
    ftalent = True if form.seeking_talent.data == 'Yes' else False
    fdescription = form.seeking_description.data.strip()
    ffacebook = form.facebook_link.data.strip()
    
    try:
      new_venue = Venues(name=fname, email=femail, phone=fphone,city=fcity,
                      state=fstate, address=faddress, website=fwebsite, 
                      image_link=fwebsite, genres=fgenres, seeking_talent=ftalent, 
                      seeking_description=fdescription, facebook_link=ffacebook)
      db.session.add(new_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('The Venue ' + fname + ' was successfully listed!')
    
    except Exception as e:
            # TODO: on unsuccessful db insert, flash an error instead.
      flash('An error occurred. Venue ' + fname + ' could not be listed. Please try again')
      db.session.rollback()
    finally:
      db.session.close()
  

  else:
    flash( form.errors )
    return redirect(url_for('create_venue_submission'))
  return render_template('pages/home.html')
  
  
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue=Venues.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  form = VenueForm(request.form)
  if form.validate_on_submit():
    try:
        venue = Venues.query.get_or_404(venue_id)

        venue.name = form.name.data
        venue.email = form.email.data
        venue.city=form.city.data
        venue.state=form.state.data
        venue.address=form.address.data
        venue.phone=form.phone.data
        venue.genres=",".join(form.genres.data) 
        venue.facebook_link=form.facebook_link.data
        venue.image_link=form.image_link.data
        venue.seeking_talent=form.seeking_talent.data
        venue.seeking_description=form.seeking_description.data
        venue.website=form.website_link.data

        # update venue on database
        db.session.add(venue)
        db.session.commit()
        flash("Venue " + form.name.data + " updated successfully")
        
    except:
        db.session.rollback()
        flash("Venue was not updated.Please try again")
    finally:
        db.session.close()
  else:
    flash("Entries not Valid.")
    
  return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  venue_user = Venues.query,filter_by(email=form.email.data)
  if venue_user:
    try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
      flash("Your Venue " + venue.name + " was deleted successfully!")
    except:
      db.session.rollback()
      print(sys.exc_info())
      flash("Problem deleting venue. Please try again")
    finally:
      db.session.close()

  return redirect(url_for("index"))
 # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None
  
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  search = request.form.get('search_term', '')
  response = {}
  venues = list(Venues.query.filter(
      Venues.name.ilike(f"%{search}%") |
      Venues.state.ilike(f"%{search}%") |
      Venues.city.ilike(f"%{search}%") 
  ).all())
  
  response["data"] = []
  response["count"] = len(venues)
  
  
  for show in venues:
    search = {
        "id": show.id,
        "name": show.name,
    }
    response["data"].append(search)

      
      
  return render_template('pages/search_venues.html', results=response, search_term=search)


@app.route('/artists')
def artists():
  data = []
  all_artist = Artists.query.all()
  for artist in all_artist:
    artist_details = {
      'id': artist.id,
      'name': artist.name
    }
    data.append(artist_details)
  
  return render_template('pages/artists.html', artists=data)



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  
  artist = Artists.query.get_or_404(artist_id)
  
  # querying data for paast show
  past_shows = []
  shows = Show.query.filter(Show.start_time <  datetime.now()).all()
  for show in shows:
    venue = Venues.query.get_or_404(show.venue_id)
    required_details ={
      'venue_id': venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      'start_time': str(show.start_time)
      }
    past_shows.append(required_details)
    
    # querying data for upcoming shows
  upcoming_shows = []
  shows = Show.query.filter(Show.start_time >= datetime.now()).all()
  for show in shows:
    venue = Venues.query.get(show.venue_id)
    required_info = {
       'venue_id': venue.id,
      "venue_name": venue.name,
      "venue_image_link": venue.image_link,
      'start_time': str(show.start_time)
      }
    upcoming_shows.append(required_info)
      
    
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  
  artists = Artists.query.filter_by(email=form.email.data).first()
  
  # setting up a minor authentication
  
  if artists:
    flash('An artist is already listed with this email')
    return redirect(url_for('create_artist_submission')) 
  
  elif form.validate_on_submit(): 
    name = form.name.data.strip()
    email = form.email.data
    city = form.city.data.strip()
    state = form.state.data.strip()
    phone = form.phone.data
    facebook_link = form.facebook_link.data
    seeking_venue = form.seeking_venue.data 
    seeking_description = form.seeking_description.data
    genres = ",".join(form.genres.data)
    website_link = form.website_link.data.strip()
    image_link = form.image_link.data.strip()
  
    try:
      new_artist = Artists(
        name=name, 
        email=email,
        city=city,
        state=state, 
        phone=phone, 
        genres=genres,
        facebook_link=facebook_link, 
        image_link=image_link,
        seeking_venue=seeking_venue,
        seeking_description=seeking_description, 
        website_link=website_link
        )
      db.session.add(new_artist)
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
      
    
    except Exception as e:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      db.session.rollback()
    finally:
      db.session.close()
  
  else:
    flash('Something went wrong during registration. Please try again')
    return redirect(url_for('create_artist_submission')) 
  return render_template('pages/home.html')

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artists.query.get_or_404(artist_id)
  #  This isn't working. I need everything i could.
  return render_template('forms/edit_artist.html',form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm()
  if form.validate_on_submit():
    try:
      artist = Artists.query.get_or_404(venue_id)

      artist.name = form.name.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.phone=form.phone.data
      artist.genres=",".join(form.genres.data) 
      artist.facebook_link=form.facebook_link.data
      artist.image_link=form.image_link.data
      artist.seeking_venue=form.seeking_venue.data
      artist.seeking_description=form.seeking_description.data
      artist.website_link=form.website_link.data

      # update venue on database
      db.session.add(artist)
      db.session.commit()
      flash("Artist profile " + form.name.data + " updated successfully")
        
    except:
        db.session.rollback()
        flash("Artist profile was not updated.Please try again")
    finally:
        db.session.close()
  else:
    flash("Entries not Valid.")

  return redirect(url_for('show_artist', artist_id=artist_id))



# search for artists

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  
  artists = Artists.query.filter( Artists.name.ilike(f"%{search_term}%") | 
                                 Artists.city.ilike(f"%{search_term}%") |
                                 Artists.state.ilike(f"%{search_term}%")).all()
                                 
  response = {"count": len(artists),"data": [] }

  for artist in artists:
      search = {}
      search["name"] = artist.name
      search["id"] = artist.id

      upcoming_shows = 0
      
      for show in artist.shows:
          if show.start_time > datetime.now():
              upcoming_shows = upcoming_shows + 1
      search["upcoming_shows"] = upcoming_shows

      response["data"].append(search)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# delete artists
@app.route("/artists/<artist_id>/delete", methods=["GET"])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
        flash("Artist " + artist.name+ " was deleted successfully!")
    except:
        db.session.rollback()
        flash("Artist was not deleted successfully.")
    finally:
        db.session.close()

    return redirect(url_for("index"))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
 
  data = []
  try:
    shows = Show.query.all()
    for show in shows:
        venue_id = show.venue_id
        artist_id = show.artist_id
        artist = Artists.query.get(artist_id)
        show_data = {
            "venue_id": venue_id,
            "venue_name": Venues.query.get(venue_id).name,
            "artist_id": artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time),
        }
        data.append(show_data)
    
  except:
    flash('Something went wrong. Please Try again')
    return redirect(url_for('index'))
    
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  
  form = ShowForm()
  
  if form.validate_on_submit():
    venue_id = form.venue_id.data
    artist_id = form.artist_id.data
    start_time = form.start_time.data
    
    try:
      # insert form data as a new Show record in the db
      new_show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
    
    except:
      db.session.rollback()
      flash('An error occurred. Show could not be listed.')
    
    finally:
      db.session.close

  else:
    return redirect(url_for('create_show_submission'))
    flash('An error occur and your entry is not valid. Please check and try again')
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''