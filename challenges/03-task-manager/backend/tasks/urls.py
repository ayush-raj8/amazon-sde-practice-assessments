from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("tasks/", views.task_list_create),
    path("tasks/<int:pk>/", views.task_detail),
    path("tasks/<int:pk>/complete/", views.mark_complete),
]
