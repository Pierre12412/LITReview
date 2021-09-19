from django.conf.urls import url
from django.urls import path

from posts import views
from posts.views import CriticsHome, TicketCreate, Review_form, CriticsMyHome, Follow

app_name = "posts"

urlpatterns = [
    path('home/',CriticsHome.as_view(),name='home'),
    path('create_ticket/',TicketCreate.as_view(),name='create ticket'),
    path('create_review/',views.Review_form,name='create review'),
    path('posts/',CriticsMyHome.as_view(),name='myposts'),
    path('followed/',Follow.as_view(),name = 'abonnements'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete')
]