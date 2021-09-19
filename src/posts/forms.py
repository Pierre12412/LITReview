from django import forms

from posts.models import Ticket, Review, UserFollows


class BookArticle(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['user']
        labels = {
            "title": "Titre",
            "description" : "Description",
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user','ticket']
        labels = {
            "headline": "Titre",
            "rating" : "Note",
            "body" : "Commentaire"
        }
        widgets = {"body": forms.Textarea()}

