import os
from requests import get
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured
from movies.models import Movie, Rating
import logging

logger = logging.getLogger(__name__)

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Translation of omdb field name -> model field name
omdb_name_mapping = {
    'Title': 'title', 'Year': 'year', 'Rated': 'rated', 'Released': 'released',
    'Runtime': 'runtime', 'Genre': 'genre', 'Director': 'director',
    'Plot': 'plot', 'Language': 'language', 'Country': 'country',
    'Awards': 'awards', 'Poster': 'poster', 'Metascore': 'metascore',
    'imdbRating': 'imdb_rating', 'imdbVotes': 'imdb_votes', 'imdbID': 'imdb_id',
    'Type': 'movie_type', 'DVD': 'dvd', 'BoxOffice': 'box_office',
    'Production': 'production', 'Website': 'website', 'Writer': 'writer',
    'Actors': 'actors',
    'Ratings': None
}

def get_data_from_omdbapi(title):
    payload = {"t": title, "apikey": OMDB_API_KEY}
    response = get('http://www.omdbapi.com/', params=payload)
    if response.status_code == 401:
        raise ImproperlyConfigured("API key missing or invalid")
    if response.status_code != 200:
        raise Exception("Can't contact movie database")
    return response

# TODO: Split decoding and saving
def omdb_to_model(json):
    logger.info("Processing movie data: {}".format(json))
    # Copy, to avoid modifying input
    json = dict(json)
    # Response isn't a part of the movie
    json.pop("Response", '')
    # TODO: (Maybe) Replace "N/A" with nulls
    # Ratings need special handling
    ratings_json = json.pop("Ratings", None)
    new_args = {omdb_name_mapping[k]: v for k, v in json.items()}
    movie = Movie(**new_args)
    # In case omdb tries to match the title more aggressively and the user tries multiple variants of the same title
    # Not using get_or_create because we want the query (not object), for url
    movie_in_db = Movie.objects.filter(title=movie.title)
    if movie_in_db.exists():
        return movie_in_db.first()
    movie.save()
    logger.info("Added new movie with id:{}, title:{}", movie.id, movie.title)
    if ratings_json is not None:
        ratings = [Rating(movie=movie, source=r['Source'], value=r['Value']) for r in ratings_json]
        Rating.objects.bulk_create(ratings)
    return movie

def get_movie_from_omdbapi(title):
    response = get_data_from_omdbapi(title)
    json = response.json()
    if json['Response'] != "True":
        logger.error("OMDB returned 'Response: false'. Response body: {}".format(json))
        raise Http404("Movie not found")
    return omdb_to_model(json)
