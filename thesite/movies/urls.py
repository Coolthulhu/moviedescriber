from django.urls import path

from movies.views import MovieView, SpecificMovieView

app_name = 'movies'

urlpatterns = [
    path('', MovieView.as_view(), name='list'),
    path("<int:pk>/", SpecificMovieView.as_view(), name='details')
]
