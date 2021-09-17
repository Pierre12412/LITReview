from django.urls import path, include
from utilisateurs.views import signup


app_name = "utilisateurs"

urlpatterns = [
    path('create_account',signup,name='signup'),
    path('',include('django.contrib.auth.urls')),
]