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
        result_list = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created,reverse=True)
        return result_list


class TicketCreate(CreateView):
    model = Ticket
    template_name = "posts/ticket_create.html"
    fields = ['title','description','image',]


class Review_form(CreateView):
    model = Review
    template_name = "posts/review_create.html"
    fields = ['headline','rating','body',]

