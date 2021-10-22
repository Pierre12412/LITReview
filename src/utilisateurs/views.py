from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from posts.forms import UserForm
from posts.models import UserFollows
from utilisateurs.models import CustomUser


def signup(request):
    context = {}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        else:
            context["errors"] = form.errors
    form = UserCreationForm()
    context["form"] = form
    return render(request, "inscription.html", context=context)


@login_required(login_url='/login')
def follow(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            users = CustomUser.objects.all()
            if request.POST.get('user_to_follow') == request.user.username:
                context['erreur'] = 'Vous ne pouvez pas ajouter vous même !'
            else:
                try:
                    for user in users:
                        if user.username == request.POST.get('user_to_follow'):
                            new_follow = UserFollows(user=request.user,
                                                     followed_user=user)
                            break
                    new_follow.save()
                    return HttpResponseRedirect('/followed')
                except UnboundLocalError:
                    context['erreur'] = 'Personne de ce nom ici ... Reéssayez'
                except IntegrityError:
                    context['erreur'] = 'Ce contact est déjà ajouté'
        else:
            print(form.errors)
    form = UserForm()
    result_abonnements = []
    result_abonnés = []
    users = CustomUser.objects.all()
    for userfollow in UserFollows.objects.all():
        if request.user.id == userfollow.followed_user_id:
            userfollow.username = userfollow.user_id
            result_abonnés.append(userfollow)
        if userfollow.user_id == request.user.id:
            userfollow.username = userfollow.followed_user_id
            result_abonnements.append(userfollow)
    for user in users:
        for abo in result_abonnés:
            if abo.username == user.id:
                abo.username = user.username
        for abonne in result_abonnements:
            if abonne.username == user.id:
                abonne.username = user.username
    context['abonnements'] = result_abonnements
    context['abonnés'] = result_abonnés
    context['form'] = form
    return render(request, "followed.html", context)


@login_required(login_url='/login')
def profile(request):
    context = {}
    context['username'] = request.user.username
    context['email'] = request.user.email
    return render(request, 'profile.html', context)