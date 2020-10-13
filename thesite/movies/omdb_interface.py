import os
import requests
from movies.models import Movie, Rating
from thesite.secrets import OMDB_API_KEY

# Translation of omdb field name -> model field name
omdb_name_mapping = {
    'Title': 'title', 'Year': 'year', 'Rated': 'rated', 'Released': 'released',
    'Runtime': 'runtime', 'Genre': 'genre', 'Director': 'director',
    'Plot': 'plot', 'Language': 'language', 'Country': 'country',
    'Awards': 'awards', 'Poster': 'poster', 'Metascore': 'metascore',
    'imdbRating': 'imdb_rating', 'imdbVotes': 'imdb_votes', 'imdbID': 'imdb_id',
    'Type': 'movie_type', 'DVD': 'dvd', 'BoxOffice': 'box_office',
    'Production': 'production', 'Website': 'website'
}

def omdb_to_model(response):
    json = response.json()
    # TODO: Replace "N/A" with nulls
    new_args = {v: json[k] for k, v in omdb_name_mapping.items() if k in json}
    movie = Movie(**new_args)
    movie.save()
    for r in json['Ratings']:
        Rating(movie=movie, source=r['Source'], value=r['Value']).save()
    return movie

def get_movie_from_omdbapi(title):
    payload = {"t": title, "apikey": OMDB_API_KEY}
    response = requests.get('http://www.omdbapi.com/', params=payload)
    return omdb_to_model(response)
