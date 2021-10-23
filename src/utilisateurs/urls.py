from django.urls import path, include
from utilisateurs.views import signup, follow, profile
from django.contrib.auth import views
app_name = "utilisateurs"

urlpatterns = [
    path('create_account', signup, name='signup'),
    path('login/', views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('followed/', follow,
         name='abonnements'),
    path('profile', profile,
         name='profil utilisateur')
]

