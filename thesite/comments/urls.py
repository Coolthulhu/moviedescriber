from django.urls import path

from comments.views import CommentListView, CommentUpdateView

app_name = 'comments'

urlpatterns = [
    path('', CommentListView.as_view(), name='index'),
    # To edit comments
    path('<int:pk>/', CommentUpdateView.as_view(), name='details'),
]
