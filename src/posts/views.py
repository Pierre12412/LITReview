from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, TemplateView
from posts.models import Ticket, Review


class CriticsHome(ListView):
    model = Ticket
    context_object_name = "tickets"

    def get_queryset(self):
        # Modify Query of tickets here
        # queryset = super().get_queryset()
        # if self.request.user.is_authenticated:
        #      return queryset
        # return queryset.filter(published = True)
        return super().get_queryset()


class TicketCreate(CreateView):
    model = Ticket
    template_name = "posts/ticket_create.html"
    fields = ['title','description','image',]


class Review_form(CreateView):
    model = Review
    template_name = "posts/review_create.html"
    fields = ['headline','rating','body',]

