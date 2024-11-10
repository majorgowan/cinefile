from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.index, name="profile_base"),
    path("profile/<str:user>", views.index, name="profile"),
    path("tmdb/<str:api_command>", views.tmdb_search, name="tmdb"),
    path("new_viewing", views.new_viewing, name="new_viewing"),
    path("delete_viewing", views.delete_viewing, name="delete_viewing"),
    path("query_viewing", views.query_viewing, name="query_viewing"),
    path("import_tool", views.import_tool, name="import_tool"),
    path("export_data", views.export_data, name="export_data"),
    path("get_session_data", views.get_session_data, name="get_session_data"),
    path("follow", views.follow, name="follow")
]