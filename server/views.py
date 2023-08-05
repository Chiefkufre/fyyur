import json
import logging
from datetime import datetime
from logging import FileHandler, Formatter

from flask import (
    Blueprint,
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .forms import ArtistForm, ShowForm, VenueForm
from .models import Artists, Show, Venues, db
from .utils import format_datetime


views = Blueprint("views", __name__)


# views.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@views.route("/")
def index():
    return render_template("pages/home.html")


@views.route("/venues")
def venues():
    data = []
    results = Venues.query.distinct(Venues.city, Venues.state).all()
    for result in results:
        city_and_state = {"city": result.city, "state": result.state}
        venues = Venues.query.filter_by(city=result.city, state=result.state).all()

        # format each venue
        formatted_venues = []
        for venue in venues:
            formatted_venues.append(
                {
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": len(
                        list(
                            filter(lambda x: x.start_time > datetime.now(), venue.shows)
                        )
                    ),
                }
            )

        city_and_state["venues"] = formatted_venues
        data.append(city_and_state)
    return render_template("pages/venues.html", areas=data)


@views.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    data = {}

    # querying the venue table
    venue_query = Venues.query.get(venue_id)

    event_before_now = (
        db.session.query(Show)
        .join(Venues)
        .filter(Show.artist_id == artist_id)
        .filter(Show.start_time < datetime.now())
        .all()
    )
    past_shows = []
    for event in event_before_now:
        artist = Artists.query.get(event.artist_id)
        artist_data = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(event.start_time),
        }
        past_shows.append(artist_data)

    new_upcoming_shows = (
        db.session.query(Show)
        .join(Venues)
        .filter(Show.artist_id == artist_id)
        .filter(Show.start_time > datetime.now())
        .all()
    )
    upcoming_shows = []
    for show in new_upcoming_shows:
        artist = Artists.query.get(show.artist_id)
        artist_data = {
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time),
        }
        upcoming_shows.append(artist_data)

    data = {
        "id": venue_query.id,
        "name": venue_query.name,
        "genres": venue_query.genres.split(","),
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
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@views.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@views.route("/venues/create", methods=["POST"])
def create_venue_submission():
    form = VenueForm()
    venue = Venues.query.filter_by(email=form.email.data).first()
    if venue:
        flash(f"Sorry, a venue is is already listed with this email: {form.email.data}")
        return render_template("pages/home.html")
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
        ftalent = True if form.seeking_talent.data == "Yes" else False
        fdescription = form.seeking_description.data.strip()
        ffacebook = form.facebook_link.data.strip()

        try:
            new_venue = Venues(
                name=fname,
                email=femail,
                phone=fphone,
                city=fcity,
                state=fstate,
                address=faddress,
                website=fwebsite,
                image_link=fwebsite,
                genres=fgenres,
                seeking_talent=ftalent,
                seeking_description=fdescription,
                facebook_link=ffacebook,
            )
            db.session.add(new_venue)
            db.session.commit()
            # on successful db insert, flash success
            flash("The Venue " + fname + " was successfully listed!")

        except Exception as e:
            print(e)
            flash(
                "An error occurred. Venue "
                + fname
                + " could not be listed. Please try again"
            )
            db.session.rollback()
        finally:
            db.session.close()

    else:
        flash(form.errors)
        return redirect(url_for("views.create_venue_submission"))
    return render_template("pages/home.html")


@views.route("/venues/<int:venue_id>/edit", methods=["GET"])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venues.query.get(venue_id)
    return render_template("forms/edit_venue.html", form=form, venue=venue)


@views.route("/venues/<int:venue_id>/edit", methods=["POST"])
def edit_venue_submission(venue_id):
    form = VenueForm(request.form)
    if form.validate_on_submit():
        try:
            venue = Venues.query.get_or_404(venue_id)

            venue.name = form.name.data
            venue.email = form.email.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.address = form.address.data
            venue.phone = form.phone.data
            venue.genres = ",".join(form.genres.data)
            venue.facebook_link = form.facebook_link.data
            venue.image_link = form.image_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data
            venue.website = form.website_link.data

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

    return redirect(url_for("views.show_venue", venue_id=venue_id))


@views.route("/venues/<venue_id>", methods=["DELETE"])
def delete_venue(venue_id):
    venue_user = Venues.query, filter_by(email=form.email.data)
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

    return redirect(url_for("views.index"))
    return None


@views.route("/venues/search", methods=["POST"])
def search_venues():
    search = request.form.get("search_term", "")
    response = {}
    venues = list(
        Venues.query.filter(
            Venues.name.ilike(f"%{search}%")
            | Venues.state.ilike(f"%{search}%")
            | Venues.city.ilike(f"%{search}%")
        ).all()
    )

    response["data"] = []
    response["count"] = len(venues)

    for show in venues:
        search = {
            "id": show.id,
            "name": show.name,
        }
        response["data"].append(search)
    return render_template(
        "pages/search_venues.html", results=response, search_term=search
    )


@views.route("/artists")
def artists():
    data = []
    all_artist = Artists.query.all()
    for artist in all_artist:
        artist_details = {"id": artist.id, "name": artist.name}
        data.append(artist_details)

    return render_template("pages/artists.html", artists=data)


@views.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    # shows the artist page with the given artist_id

    artist = Artists.query.get_or_404(artist_id)

    # querying data for paast show
    past_shows = []
    shows = Show.query.filter(Show.start_time < datetime.now()).all()
    for show in shows:
        venue = Venues.query.get_or_404(show.venue_id)
        required_details = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(show.start_time),
        }
        past_shows.append(required_details)

        # querying data for upcoming shows
    upcoming_shows = []
    shows = Show.query.filter(Show.start_time >= datetime.now()).all()
    for show in shows:
        venue = Venues.query.get(show.venue_id)
        required_info = {
            "venue_id": venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": str(show.start_time),
        }
        upcoming_shows.append(required_info)

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(","),
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
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_artist.html", artist=data)


#  Create Artist
#  ----------------------------------------------------------------


@views.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@views.route("/artists/create", methods=["POST"])
def create_artist_submission():
    form = ArtistForm(request.form)

    artists = Artists.query.filter_by(email=form.email.data).first()

    # setting up a minor authentication

    if artists:
        flash("An artist is already listed with this email")
        return redirect(url_for("views.create_artist_submission"))

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
                website_link=website_link,
            )
            db.session.add(new_artist)
            db.session.commit()
            flash("Artist " + request.form["name"] + " was successfully listed!")

        except Exception as e:
            flash(
                "An error occurred. Artist "
                + request.form["name"]
                + " could not be listed."
            )
            db.session.rollback()
        finally:
            db.session.close()

    else:
        flash("Something went wrong during registration. Please try again")
        return redirect(url_for("views.create_artist_submission"))
    return render_template("pages/home.html")


#  Update
#  ----------------------------------------------------------------
@views.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artists.query.get_or_404(artist_id)
    #  This isn't working. I need everything i could.
    return render_template("forms/edit_artist.html", form=form, artist=artist)


@views.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm()
    if form.validate_on_submit():
        try:
            artist = Artists.query.get_or_404(venue_id)

            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = ",".join(form.genres.data)
            artist.facebook_link = form.facebook_link.data
            artist.image_link = form.image_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data
            artist.website_link = form.website_link.data

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

    return redirect(url_for("views.show_artist", artist_id=artist_id))


# search for artists


@views.route("/artists/search", methods=["POST"])
def search_artists():
    search_term = request.form.get("search_term", "")

    artists = Artists.query.filter(
        Artists.name.ilike(f"%{search_term}%")
        | Artists.city.ilike(f"%{search_term}%")
        | Artists.state.ilike(f"%{search_term}%")
    ).all()

    response = {"count": len(artists), "data": []}

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
    return render_template(
        "pages/search_artists.html",
        results=response,
        search_term=request.form.get("search_term", ""),
    )


# Delete artists function
@views.route("/artists/<artist_id>/delete", methods=["GET"])
def delete_artist(artist_id):
    try:
        artist = Artist.query.get(artist_id)
        db.session.delete(artist)
        db.session.commit()
        flash("Artist " + artist.name + " was deleted successfully!")
    except:
        db.session.rollback()
        flash("Artist was not deleted successfully.")
    finally:
        db.session.close()

    return redirect(url_for("views.index"))


#  Shows
#  ----------------------------------------------------------------


@views.route("/shows")
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
        flash("Something went wrong. Please Try again")
        return redirect(url_for("views.index"))

    return render_template("pages/shows.html", shows=data)


@views.route("/shows/create")
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@views.route("/shows/create", methods=["POST"])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form

    form = ShowForm()

    if form.validate_on_submit():
        venue_id = form.venue_id.data
        artist_id = form.artist_id.data
        start_time = form.start_time.data

        try:
            # insert form data as a new Show record in the db
            new_show = Show(
                venue_id=venue_id, artist_id=artist_id, start_time=start_time
            )
            db.session.add(new_show)
            db.session.commit()
            flash("Show was successfully listed!")

        except:
            db.session.rollback()
            flash("An error occurred. Show could not be listed.")

        finally:
            db.session.close

    else:
        return redirect(url_for("views.create_show_submission"))
        flash("An error occur and your entry is not valid. Please check and try again")
    return render_template("pages/home.html")


@views.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@views.errorhandler(500)
def server_error(error):
    return render_template("errors/500.html"), 500


# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()
