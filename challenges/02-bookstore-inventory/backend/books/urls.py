from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("books/", views.list_or_create_books),
    path("books/<int:pk>/", views.book_detail),
]
