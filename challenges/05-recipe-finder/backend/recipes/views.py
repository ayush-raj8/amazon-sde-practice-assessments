"""
Recipe search endpoints.

Product requirements (read carefully):
- POST /api/recipes/search/ body may include:
    ingredients: list of strings — recipe ingredients field must contain ALL
                 as substrings (AND).
    cuisine: optional icontains match.
    diet: optional — any/omitted = no filter; vegetarian matches vegetarian OR vegan;
          vegan matches vegan only.
    max_cook_time: optional int — cook_time_minutes <= max_cook_time.
"""

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Recipe
from .serializers import RecipeSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "challenge": "recipe-finder"})


@api_view(["GET"])
def list_recipes(request):
    qs = Recipe.objects.all().order_by("name")
    return Response(RecipeSerializer(qs, many=True).data)


@api_view(["POST"])
def search_recipes(request):
    """
    Body JSON may include:
      ingredients (list[str]), cuisine (str), diet (str), max_cook_time (int)
    Empty / missing optional filters are ignored.
    """
    data = request.data or {}
    ingredients = data.get("ingredients") or []
    if isinstance(ingredients, str):
        ingredients = [p.strip() for p in ingredients.split(",") if p.strip()]
    else:
        ingredients = [str(i).strip() for i in ingredients if str(i).strip()]

    cuisine = (data.get("cuisine") or "").strip()
    diet = (data.get("diet") or "").strip().lower()
    max_cook_time = data.get("max_cook_time")

    qs = Recipe.objects.all()
    applied = False

    if ingredients:
        condition = Q()
        for term in ingredients:
            condition |= Q(ingredients__icontains=term)
        qs = qs.filter(condition)
        applied = True

    if cuisine:
        qs = qs.filter(cuisine__icontains=cuisine)
        applied = True

    if diet and diet != "any":
        qs = qs.filter(diet=diet)
        applied = True

    if max_cook_time not in (None, ""):
        try:
            minutes = int(max_cook_time)
        except (TypeError, ValueError):
            return Response({"error": "max_cook_time must be an integer"}, status=400)
        qs = qs.filter(cook_time_minutes__gte=minutes)
        applied = True

    if not applied:
        qs = Recipe.objects.none()

    return Response(RecipeSerializer(qs.order_by("name"), many=True).data)
