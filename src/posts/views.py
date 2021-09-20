from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView, CreateView
from posts.forms import BookArticle, ReviewForm, UserFollow, UserForm
from posts.models import Ticket, Review, UserFollows
from itertools import chain

class CriticsHome(ListView):
    model = Ticket
    context_object_name = "posts"
    template_name = 'posts/ticket_list.html'

    def get_queryset(self):
        follow = [self.request.user.id]
        users = User.objects.all()
        users_follow = UserFollows.objects.filter(user_id=self.request.user.id)
        for user in users_follow:
            for all_user in users:
                if all_user.id == user.followed_user_id:
                    follow.append(all_user.id)


        all_reviews = Review.objects.all()
        all_tickets = Ticket.objects.filter(user_id=self.request.user.id)
        review_id = []
        ticket_id = []
        for review in all_reviews:
            for ticket in all_tickets:
                if review.ticket_id == ticket.id:
                    review_id.append(review.id)
        for review in all_reviews:
            if review.user_id == self.request.user.id:
                ticket_id.append(review.ticket_id)

        tickets = Ticket.objects.filter(Q(user_id__in = follow) | Q(id__in = ticket_id))
        reviews = Review.objects.filter(Q(user_id__in = follow) | Q(id__in = review_id))
        for ticket in tickets:
            for user in users:
                if ticket.user_id == user.id:
                    ticket.username = user.username
        for review in reviews:
            for user in users:
                if review.user_id == user.id:
                    review.username = user.username
            for ticket in tickets:
                if review.ticket_id == ticket.id:
                    review.ticket = ticket
                    ticket.already = True

        result_list = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created,reverse=True)
        return result_list


class TicketCreate(CreateView):
    model = Ticket
    template_name = "posts/ticket_create.html"
    fields = ['title','description','image',]

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.user= self.request.user
        model_instance.save()
        return HttpResponseRedirect('/home')


def Review_form(request,ticket=None,review=None):
    try:
        ticket = Ticket.objects.filter(id=ticket)[0]
    except:
        pass
    try:
        reviews = Review.objects.filter(id=review)[0]
    except:
        pass
    if request.method == 'POST':
        form = BookArticle(request.POST)
        formset = ReviewForm(request.POST)
        if form.is_valid() or formset.is_valid():
            if reviews == None:
                instance_review = formset.save(commit=False)
                try:
                    instance_ticket = form.save(commit=False)
                    instance_ticket.user_id = request.user.id
                    instance_ticket.save()
                    instance_review.user_id = request.user.id
                    instance_review.ticket_id = instance_ticket.pk
                except:
                    instance_review.user_id = request.user.id
                    instance_review.ticket_id = ticket.id
                instance_review.save()
                return HttpResponseRedirect('/posts/')
            else:
                reviews.rating = request.POST.get('rating')
                reviews.headline = request.POST.get('headline')
                reviews.body = request.POST.get('body')
                reviews.save()
                return HttpResponseRedirect('/posts/')
    try:
        form_review = ReviewForm(initial={'headline':reviews.headline,'rating':reviews.rating,'body':reviews.body})
    except:
        form_review = ReviewForm()
    form_ticket = BookArticle()
    return render(request,"posts/review_create.html",{"ticket_form":form_ticket,"review_form":form_review, "ticket":ticket})

class CriticsMyHome(ListView):
    model = Ticket
    context_object_name = "posts"
    template_name = 'posts/mypost.html'

    def get_queryset(self):
        all_tickets = Ticket.objects.all()
        tickets = Ticket.objects.filter(user_id=self.request.user.id)
        reviews = Review.objects.filter(user_id=self.request.user.id)
        users = User.objects.all()
        for review in reviews:
            for ticket in all_tickets:
                if ticket.id == review.ticket_id:
                    review.ticket = ticket
        for review in reviews:
            review.username = self.request.user.username
        for ticket in tickets:
            ticket.username = self.request.user.username
        for user in users:
            for review in reviews:
                if review.ticket.user_id == user.id:
                    review.ticket.username = user.username
        result_list = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created,reverse=True)
        return result_list

def delete(request,id):
    to_delete = get_object_or_404(UserFollows, pk=id).delete()
    return HttpResponseRedirect('/followed')

def follow(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            users = User.objects.all()
            try:
                for user in users:
                    if user.username == request.POST.get('user_to_follow'):
                        new_follow = UserFollows(user=request.user,followed_user=user)
                        break
                new_follow.save()
                return HttpResponseRedirect('/followed')
            except:
                context['erreur'] = 'Personne de ce nom ici ... Reéssayez'
        else:
            print(form.errors)
    form = UserForm()
    result_abonnements = []
    result_abonnés = []
    users = User.objects.all()
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
    return render(request, "followed.html",context)

def delete_post(request,id):
    get_object_or_404(Ticket, pk=id).delete()
    return HttpResponseRedirect('/posts')

def update_post(request,id):
    get_object_or_404(UserFollows, pk=id).update()
    return HttpResponseRedirect('/posts')

def delete_review(request,id):
    get_object_or_404(Review, pk=id).delete()
    return HttpResponseRedirect('/posts')