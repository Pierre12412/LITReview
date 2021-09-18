from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from posts.models import Ticket, Review, UserFollows
from itertools import chain

class CriticsHome(ListView):
    model = Ticket
    context_object_name = "posts"
    template_name = 'posts/ticket_list.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter()
        reviews = Review.objects.filter()
        users = User.objects.all()
        for review in reviews:
            for user in users:
                if review.user_id == user.id:
                    review.username = user.username
        for ticket in tickets:
            for user in users:
                if ticket.user_id == user.id:
                    ticket.username = user.username
        for review in reviews:
            for ticket in tickets:
                if review.ticket_id == ticket.id:
                    review.ticket = ticket
        for review in reviews:
            for ticket in tickets:
                if review.ticket_id == ticket.id:
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


class Review_form(CreateView):
    model = Review
    template_name = "posts/review_create.html"
    fields = ['headline','rating','body',]

class CriticsMyHome(ListView):
    model = Ticket
    context_object_name = "posts"
    template_name = 'posts/mypost.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter(user_id=self.request.user.id)
        reviews = Review.objects.filter(user_id=self.request.user.id)
        for review in reviews:
            review.username = self.request.user.username
        for ticket in tickets:
            ticket.username = self.request.user.username
        for review in reviews:
            for ticket in tickets:
                if review.ticket_id == ticket.id:
                    review.ticket = ticket
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
