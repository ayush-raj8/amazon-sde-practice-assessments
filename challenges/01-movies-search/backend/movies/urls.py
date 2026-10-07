from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("movies/", views.list_movies),
    path("movies/search/", views.simple_search),
    path("movies/advanced-search/", views.advanced_search),
]
