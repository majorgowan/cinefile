from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("settings/", views.settings, name="settings"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),
]