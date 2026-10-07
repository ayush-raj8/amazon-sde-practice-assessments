"""
App URLConf for `events`.

Mounted under /api/ by config/urls.py.

  GET /api/events/           → list_events
  GET /api/events/?club=<id> → list_events (filtered)
"""

from django.urls import path

from . import views

urlpatterns = [
    path("events/", views.list_events),
]
