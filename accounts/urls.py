from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("settings/", views.settings, name="settings"),
]