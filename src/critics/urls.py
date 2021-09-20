from django.contrib import admin
from django.urls import path, include

from utilisateurs.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', signup, name='register'),
    path('',include('posts.urls')),
    path('',include('utilisateurs.urls')),
]
