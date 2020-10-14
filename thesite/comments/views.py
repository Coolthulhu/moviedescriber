from django.forms.models import model_to_dict
from django.db.models import Count, Window, F, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from django.db.models.functions import DenseRank
from comments.models import Comment
from comments.forms import AddCommentForm, CommentForm, GetCommentsForm, GetTopForm
from movies.models import Movie
import datetime

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponseNotFound

"""Lists comments, filtered by movie id if provided."""
class CommentListView(View):
    def get(self, request):
        form = GetCommentsForm(request.GET)
        # Just validate, treat errors as if no filtering was enabled
        form.is_valid()
        id = form.cleaned_data.get('id', None)
        comments = Comment.objects
        if id is not None:
            comments = comments.filter(movie__id=id)
        # ID added for easier comment editing
        comments = comments.values('id', 'movie', 'text', 'date')
        return JsonResponse(list(comments.all()), safe=False)

    # TODO: Use CreateView
    def post(self, request):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            movie = form.cleaned_data['movie']
            now = datetime.datetime.now().date()
            Comment(movie=movie, text=form.cleaned_data['text'], date=now).save()
            # Redirect to self turns POST to GET
            return redirect(request.path)
        elif 'movie' in form.errors:
            return HttpResponseNotFound("No movie with id {}".format(form.data['movie']))
        else:
            return HttpResponseBadRequest("Text too long")

"""Convenient view for changing comment date."""
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment.html"

def top_view(request):
    form = GetTopForm(request.GET)
    if not form.is_valid():
        return HttpResponseBadRequest("Invalid params: {}".format(form.errors))
    start_date = form.cleaned_data['start_date']
    end_date = form.cleaned_data['end_date']
    commented = get_ranked_movies(start_date, end_date)
    return JsonResponse(list(commented), safe=False)

def get_ranked_movies(start_date, end_date):
    return (
        Movie.objects.all()
        # Renaming id to movie_id
        .annotate(movie_id=F('id'), 
        # Only count comments in the range
            total_comments=Count('comment', filter=Q(comment__date__range=(start_date, end_date))))
        # Rank is higher for a movie with lower number of comments
        # Equal for same number
        # Is dense (no gaps)
        # Equals 1 for the most commented movie
        .annotate(rank=Window(
            expression=DenseRank(),
            order_by=F('total_comments').desc(),
        ))
        .order_by('rank')
        .values('movie_id', 'total_comments', 'rank')
    )
