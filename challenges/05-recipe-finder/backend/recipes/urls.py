from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("recipes/", views.list_recipes),
    path("recipes/search/", views.search_recipes),
]
