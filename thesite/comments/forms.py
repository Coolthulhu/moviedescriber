from django.forms import Form, ModelForm, DateField
from django import forms
from comments.models import Comment

class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['movie', 'text']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['movie', 'text', 'date']

class GetCommentsForm(Form):
    id = forms.IntegerField(required=False)

class GetTopForm(Form):
    start_date = DateField()
    end_date = DateField()
