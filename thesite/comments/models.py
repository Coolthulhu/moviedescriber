from django.db.models import Model, ForeignKey, CharField, DateField, CASCADE, Index
from django.urls import reverse
from movies.models import Movie

class Comment(Model):
    movie = ForeignKey(Movie, on_delete=CASCADE)
    text = CharField(max_length=10000)
    date = DateField()

    class Meta:
        indexes = [
            Index(fields=['movie']),
            Index(fields=['date']),
        ]

    def get_absolute_url(self):
        return reverse('comments:details', kwargs={'pk': self.id})
