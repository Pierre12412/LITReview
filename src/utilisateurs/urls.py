from django.shortcuts import redirect
from django.urls import path, include
from utilisateurs.views import signup


app_name = "utilisateurs"

urlpatterns = [
    path('account/create',signup,name='signup'),
    path('',include('django.contrib.auth.urls')),
]