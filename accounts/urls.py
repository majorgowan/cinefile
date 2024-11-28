from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("settings/", views.settings, name="settings"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),
    # mobile views
    path("m/signup/", views.mobile_signup, name="mobile_signup"),
    path("m/login/", views.mobile_user_login, name="mobile_user_login"),
    path("m/settings/", views.mobile_settings, name="mobile_settings"),
    path("m/change_password/", views.mobile_change_password,
         name="mobile_change_password"),
    path("m/delete_account/", views.mobile_delete_account,
         name="mobile_delete_account"),
]