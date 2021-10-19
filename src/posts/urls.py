from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path

from posts import views
from posts.views import CriticsHome, TicketCreate, CriticsMyHome
from django.conf import settings
from django.conf.urls.static import static

app_name = "posts"

urlpatterns = [
     path('home/', login_required(CriticsHome.as_view(),
                                  login_url='/login'),
          name='home'),
     path('create_ticket/', login_required(TicketCreate.as_view(),
                                           login_url='/login'),
          name='create ticket'),
     path('create_ticket/<int:ticket>', views.update_post,
          name='update ticket'),
     path('create_review/', views.Review_form,
          name='create review'),
     path('create_review/<int:ticket>', views.Review_form,
          name='create review ticket'),
     path('create_review/<int:ticket>/<int:review>', views.Review_form,
          name='create review ticket'),
     path('posts/', login_required(CriticsMyHome.as_view(),
                                   login_url='/login'),
          name='myposts'),
     url(r'^delete/(?P<id>\d+)/$', views.delete,
         name='delete'),
     url(r'^posts/ticket/delete/(?P<id>\d+)/$', views.delete_post,
         name='delete'),
     url(r'^posts/review/delete/(?P<id>\d+)/$', views.delete_review,
         name='delete')
     ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
