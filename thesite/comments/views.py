from django.forms.models import model_to_dict
from django.db.models import Count, Window, F, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView
from django.db.models.functions import DenseRank
from comments.models import Comment
from comments.forms import AddCommentForm, CommentForm, GetTopForm
from movies.models import Movie
import datetime

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect, HttpResponseNotFound

"""Lists comments, filtered by movie id if provided."""
class CommentListView(ListView):
    model = Comment

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            id = self.request.GET.get('id')
            return queryset.filter(id=int(id))
        except ValueError:
            pass
        return queryset

    # TODO: Use CreateView
    def post(self, request):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['movie']
            movie_in_db = Movie.objects.filter(id=id)
            if movie_in_db.exists():
                now = datetime.datetime.now().date()
                Comment(movie=movie_in_db.first(), text=form.cleaned_data['text'], date=now).save()
            else:
                return HttpResponseNotFound("No movie with id {}".format(id))
            # Redirect to self should turn POST to GET
            return redirect(request.path)
        else:
            return HttpResponseBadRequest(form.errors)

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
    commented = (
        Movie.objects.all()
        # Renaming id to movie_id
        .annotate(movie_id=F('id'), 
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
    return JsonResponse(list(commented), safe=False)
