"""
Project URLConf — the top of the routing tree.

Trace example for GET /api/clubs/?category=sports
  1. settings.ROOT_URLCONF → this file
  2. path("api/", include("clubs.urls")) strips "api/" and forwards "clubs/?…"
  3. clubs/urls.py matches "clubs/" → clubs.views.list_or_create_clubs
  4. That view function runs and returns JSON

Trace example for POST /api/events/3/cancel/
  1. This file → include("events.urls")
  2. events/urls.py → find the pattern "events/<pk>/cancel/"
  3. Open the *view name* on that path — confirm it is the function you expect
"""

from django.urls import include, path

urlpatterns = [
    # Health lives in the clubs app but is mounted under /api/health/
    path("api/", include("clubs.urls")),
    path("api/", include("events.urls")),
]
