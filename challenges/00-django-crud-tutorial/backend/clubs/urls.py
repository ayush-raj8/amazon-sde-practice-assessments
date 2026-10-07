"""
App URLConf for `clubs`.

Mounted under /api/ by config/urls.py.

  GET /api/health/  → health
  GET /api/clubs/   → list_clubs
"""

from django.urls import path

from . import views

urlpatterns = [
    path("health/", views.health),
    path("clubs/", views.list_clubs),
]
