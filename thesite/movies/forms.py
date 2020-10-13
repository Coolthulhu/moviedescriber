from django.forms import Form, ModelForm, CharField
from movies.models import Movie, Rating
from comments.models import Comment
from django.forms.models import inlineformset_factory


class AddMovieForm(Form):
    title = CharField()

class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        exclude = ['id']

# Ratings require special handling because they're in an array
RatingFormset = inlineformset_factory(
    Movie, Rating, fields=('source', 'value'), extra=1
)
