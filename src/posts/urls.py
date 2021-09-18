from django.urls import path
from posts.views import CriticsHome, TicketCreate, Review_form, CriticsMyHome

app_name = "posts"

urlpatterns = [
    path('home/',CriticsHome.as_view(),name='home'),
    path('create_ticket/',TicketCreate.as_view(),name='create ticket'),
    path('create_review/',Review_form.as_view(),name='create review'),
    path('posts/',CriticsMyHome.as_view(),name='myposts'),
]