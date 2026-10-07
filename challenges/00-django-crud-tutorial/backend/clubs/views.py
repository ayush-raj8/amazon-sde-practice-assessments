"""
Clubs app — list endpoint.

Request lands here only after:
  settings.ROOT_URLCONF → config/urls.py → include("clubs.urls") → this path.
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Club
from .serializers import ClubSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "challenge": "django-crud-tutorial"})


@api_view(["GET"])
def list_clubs(request):
    qs = Club.objects.all().order_by("name")
    return Response(ClubSerializer(qs, many=True).data)
