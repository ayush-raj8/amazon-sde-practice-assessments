from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("employees/", views.list_employees),
]
