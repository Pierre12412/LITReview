from django.conf.urls import url
from django.urls import path

from posts import views
from posts.views import CriticsHome, TicketCreate, CriticsMyHome, follow

app_name = "posts"

urlpatterns = [
     path('home/', CriticsHome.as_view(),
          name='home'),
     path('create_ticket/', TicketCreate.as_view(),
          name='create ticket'),
     path('create_ticket/<int:ticket>', views.update_post,
          name='update ticket'),
     path('create_review/', views.Review_form,
          name='create review'),
     path('create_review/<int:ticket>', views.Review_form,
          name='create review ticket'),
     path('create_review/<int:ticket>/<int:review>', views.Review_form,
          name='create review ticket'),
     path('posts/', CriticsMyHome.as_view(),
          name='myposts'),
     path('followed/', follow,
          name='abonnements'),
     url(r'^delete/(?P<id>\d+)/$', views.delete,
         name='delete'),
     url(r'^posts/ticket/delete/(?P<id>\d+)/$', views.delete_post,
         name='delete'),
     url(r'^posts/review/delete/(?P<id>\d+)/$', views.delete_review,
         name='delete')
]
