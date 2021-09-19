from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django.views.generic import ListView, CreateView
from posts.forms import BookArticle, ReviewForm
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
        tickets = Ticket.objects.filter(user_id__in = follow)
        reviews = Review.objects.filter(user_id__in = follow)
        for review in reviews:
            for user in users:
                if review.user_id == user.id:
                    review.username = user.username
            for ticket in tickets:
                if review.ticket_id == ticket.id:
                    review.ticket = ticket
                    ticket.already = True
        for ticket in tickets:
            for user in users:
                if ticket.user_id == user.id:
                    ticket.username = user.username

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


def Review_form(request,ticket=None):
    try:
        ticket = Ticket.objects.filter(id=ticket)[0]
    except:
        pass
    if request.method == 'POST':
        print(request.POST)
        form = BookArticle(request.POST)
        formset = ReviewForm(request.POST)
        if form.is_valid() or formset.is_valid():
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
    form_ticket = BookArticle()
    form_review = ReviewForm()
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

class Follow(CreateView):
    model = UserFollows
    context_object_name = "abonnés"
    template_name = 'followed.html'
    fields = ['followed_user']

    def form_valid(self, form):
        model_instance = form.save(commit=False)
        model_instance.user = self.request.user
        model_instance.save()
        return HttpResponseRedirect('/followed')

    def get_context_data(self, *args, **kwargs):
        result_abonnements = []
        result_abonnés = []
        users = User.objects.all()
        context = super().get_context_data(*args, **kwargs)
        for userfollow in UserFollows.objects.all():
            if self.request.user.id == userfollow.followed_user_id:
                userfollow.username = userfollow.user_id
                result_abonnés.append(userfollow)
            if userfollow.user_id == self.request.user.id:
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
        return context


def delete(request,id):
    to_delete = get_object_or_404(UserFollows, pk=id).delete()
    return HttpResponseRedirect('/followed')