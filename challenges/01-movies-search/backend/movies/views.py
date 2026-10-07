"""
Movie search endpoints.

Product requirements (read carefully):
- Simple search: query `q` + `field` in {all, title, director, description, cast}.
  Search must look in the selected field (or all of them when field=all).
- Advanced search: optional filters title, director, description, cast, genre, year.
  When multiple filters are provided, results must match ALL of them (AND).
"""

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "challenge": "movies-search"})


@api_view(["GET"])
def list_movies(request):
    qs = Movie.objects.all().order_by("title")
    return Response(MovieSerializer(qs, many=True).data)


@api_view(["GET"])
def simple_search(request):
    q = (request.GET.get("q") or "").strip()
    field = (request.GET.get("field") or "all").strip().lower()

    if not q:
        return Response([])

    qs = Movie.objects.filter(title__icontains=q)
    return Response(MovieSerializer(qs.order_by("title"), many=True).data)


@api_view(["POST"])
def advanced_search(request):
    """
    Body JSON may include any of:
      title, director, description, cast, genre, year
    Empty / missing filters are ignored.
    Multiple present filters must ALL match (AND).
    """
    data = request.data or {}
    title = (data.get("title") or "").strip()
    director = (data.get("director") or "").strip()
    description = (data.get("description") or "").strip()
    cast = (data.get("cast") or "").strip()
    genre = (data.get("genre") or "").strip()
    year = data.get("year")

    condition = Q()
    if title:
        condition |= Q(title__icontains=title)
    if director:
        condition |= Q(director__icontains=director)
    if description:
        condition |= Q(description__icontains=description)
    if cast:
        condition |= Q(cast__icontains=cast)
    if genre:
        condition |= Q(genre__icontains=genre)
    if year not in (None, ""):
        try:
            condition |= Q(year=int(year))
        except (TypeError, ValueError):
            return Response({"error": "year must be an integer"}, status=400)

    if condition == Q():
        qs = Movie.objects.none()
    else:
        qs = Movie.objects.filter(condition)

    return Response(MovieSerializer(qs.order_by("title"), many=True).data)
