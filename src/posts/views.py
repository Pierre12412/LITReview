from datetime import datetime

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from posts.models import Ticket, Review
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
    template_name = 'posts/ticket_list.html'

    def get_queryset(self):
        tickets = Ticket.objects.filter(user_id=self.request.user.id)
        reviews = Review.objects.filter(user_id=self.request.user.id)
        users = User.objects.all()
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