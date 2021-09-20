from django import forms
from django.contrib.auth.models import User

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


class UserFollow(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
        labels = {
            "followed_user": "Utilisateur à suivre",
        }
        widgets = {"followed_user" : forms.TextInput()}

class UserForm(forms.Form):
    users = User.objects.all()
    CHOICES = ()
    for user in users :
        CHOICES = CHOICES + ((user,user.username),)
    user_to_follow = forms.ChoiceField(choices=CHOICES,label='Utilisateur à ajouter')

    def __init__(self,*args,**kwargs):
        self.user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)
        users = User.objects.all()
        CHOICES = ()
        for user in users:
            if user.username != self.user.username:
                CHOICES = CHOICES + ((user, user.username),)
        self.fields['user_to_follow'] = forms.ChoiceField(choices=CHOICES,label='Utilisateur à ajouter')
