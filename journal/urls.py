from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="profile"),
    path("profile/<str:user>", views.index, name="profile"),
    path("tmdb/<str:api_command>", views.tmdb_search, name="tmdb"),
    path("new_viewing", views.new_viewing, name="new_viewing"),
    path("query_viewing", views.query_viewing, name="query_viewing"),
    path("import_tool", views.import_tool, name="import_tool"),
    path("get_session_data", views.get_session_data, name="get_session_data")
]