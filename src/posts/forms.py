from django import forms

from posts.models import Ticket, Review, UserFollows
from utilisateurs.models import CustomUser


class BookArticle(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['user']
        labels = {
            "title": "Titre",
            "description": "Description",
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ['user', 'ticket']
        labels = {
            "headline": "Titre",
            "rating": "Note",
            "body": "Commentaire"
        }
        widgets = {"body": forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'] = forms.IntegerField(max_value=5, min_value=1)


class UserFollow(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        labels = {
            "followed_user": "Utilisateur à suivre",
        }
        widgets = {"followed_user": forms.TextInput()}


class UserForm(forms.Form):
    users = CustomUser.objects.all()
    user_to_follow = forms.CharField(label='Utilisateur à ajouter')
