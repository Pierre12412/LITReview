from django.shortcuts import render

from django.views.generic import ListView
from posts.models import Ticket

class CriticsHome(ListView):
    model = Ticket
    context_object_name = "tickets"
