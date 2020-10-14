from django.db import models
from django.urls import reverse

class Movie(models.Model):
    # Values as strings because it's more convenient here
    # Might be cleaner to have them nullable
    title = models.CharField(max_length=200, verbose_name="Title")
    year = models.CharField(max_length=100, verbose_name="Year")
    rated = models.CharField(max_length=100, verbose_name="Rated")
    released = models.CharField(max_length=100, verbose_name="Released")
    runtime = models.CharField(max_length=100, verbose_name="Runtime")
    genre = models.CharField(max_length=1000, verbose_name="Genre")
    director = models.CharField(max_length=100, verbose_name="Director")
    plot = models.CharField(max_length=10000, verbose_name="Plot")
    language = models.CharField(max_length=100, verbose_name="Language")
    country = models.CharField(max_length=100, verbose_name="Country")
    awards = models.CharField(max_length=100, verbose_name="Awards")
    poster = models.CharField(max_length=1000, verbose_name="Poster URL")
    metascore = models.CharField(max_length=100, verbose_name="Metascore")
    imdb_rating = models.CharField(max_length=100, verbose_name="IMDB rating")
    imdb_votes = models.CharField(max_length=100, verbose_name="IMDB votes")
    imdb_id = models.CharField(max_length=100, verbose_name="IMDB ID")
    movie_type = models.CharField(max_length=100, verbose_name="Type")
    dvd = models.CharField(max_length=100, verbose_name="DVD")
    box_office = models.CharField(max_length=100, verbose_name="Box office")
    production = models.CharField(max_length=100, verbose_name="Production")
    website = models.CharField(max_length=100, verbose_name="Website")
    writer = models.CharField(max_length=100, verbose_name="Writer")
    actors = models.CharField(max_length=1000, verbose_name="Actors")

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]
        constraints = [
            models.UniqueConstraint(fields=['title'], name="unique_title"),
        ]

    def get_absolute_url(self):
        return reverse('movies:details', kwargs={'pk': self.id})

class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['movie'])
        ]
