import imp
from re import template
from django.urls import path
from django.contrib.auth import views
from .views import register, logout_view, profile


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('register/', register, name="register"),
    path('logout/', logout_view, name="logout"),
    path('profile/', profile, name="profile")
]