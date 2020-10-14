from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from movies.forms import AddMovieForm, MovieModelForm
from movies.models import Movie, Rating
import requests

from django.urls import resolve
from urllib.parse import urlencode

from django.forms.models import model_to_dict
from django.core import serializers

from django.views import generic, View
from django.views.generic.edit import UpdateView

from movies.forms import RatingFormset
from movies.omdb_interface import get_movie_from_omdbapi

import json

class MovieView(generic.ListView):
    model = Movie
    ordering = "title"

    def post(self, request):
        form = AddMovieForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            # First check the db
            # Not specified in requirements: should it error, allow duplicates, just use the existing copy?
            movie_in_db = Movie.objects.filter(title=title)
            if movie_in_db.exists():
                return redirect(movie_in_db.first().get_absolute_url())
            movie = get_movie_from_omdbapi(title)
            # In case omdb tries to match the title more aggressively and the user tries multiple variants of the same title
            movie_in_db = Movie.objects.filter(title=movie.title)
            if not movie_in_db.exists():
                movie.save()
                movie_in_db = Movie.objects.filter(id=movie.id)

            return redirect(movie_in_db.first().get_absolute_url())
        else:
            return HttpResponseBadRequest(form.errors)

class SpecificMovieView(UpdateView):
    model = Movie
    form_class = MovieModelForm
    template_name = "movies/movie.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = RatingFormset(instance=self.object)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = RatingFormset(self.request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return self.get(request)
        return HttpResponseBadRequest("Form errors: {}<br>Formset errors: {}".format(form.errors, formset.errors))

    def delete(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        title = movie.title
        movie.delete()
        return HttpResponse("Deleted movie {}".format(title))

    def put(self, request, pk):
        # Not using get_object_or_404 because Model doesn't have update
        movie_from_db = Movie.objects.filter(id=pk)
        if not movie_from_db.exists():
            return HttpResponseNotFound("No movie with id {} exists".format(pk))
        # TODO: Error handling
        js = json.loads(request.body)
        movie_from_db.update(**js)
        return HttpResponse("Updated movie with id {}".format(pk))
