from django.urls import path
from posts.views import CriticsHome

app_name = "posts"

urlpatterns = [
    path('',CriticsHome.as_view(),name='home')
]