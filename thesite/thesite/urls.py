from django.contrib import admin
from django.urls import include, path
from comments.views import top_view

urlpatterns = [
    path('', include('ui.urls'), name="ui"),
    path('movies/', include('movies.urls', 'movies'), name="movies"),
    path('comments/', include('comments.urls', 'comments'), name="comments"),
    path('top/', top_view, name="top"),
    path('admin/', admin.site.urls),
]
