"""
Acceptance tests for recipe search.

These fail on the buggy starter code and pass once the candidate fixes behavior.
"""

import os
import sys

import pytest

BACKEND = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, BACKEND)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.core.management import call_command
from rest_framework.test import APIClient

from recipes.models import Recipe


@pytest.fixture(autouse=True)
def _db(tmp_path, settings):
    settings.DATABASES["default"]["NAME"] = str(tmp_path / "test.sqlite3")
    call_command("migrate", verbosity=0, interactive=False)
    call_command("seed_recipes", verbosity=0)
    return APIClient()


@pytest.fixture
def client(_db):
    return _db


def test_health(client):
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_ingredients_require_all(client):
    """tomato AND basil must not return recipes that only have one of them."""
    res = client.post(
        "/api/recipes/search/",
        {"ingredients": ["tomato", "basil"]},
        format="json",
    )
    assert res.status_code == 200
    names = {r["name"] for r in res.json()}
    assert names == {"Tomato Basil Pasta"}


def test_max_cook_time_is_upper_bound(client):
    res = client.post(
        "/api/recipes/search/",
        {"max_cook_time": 30},
        format="json",
    )
    assert res.status_code == 200
    names = {r["name"] for r in res.json()}
    assert names == {
        "Tomato Basil Pasta",
        "Tomato Soup",
        "Veggie Stir Fry",
        "Beef Tacos",
        "Miso Soup",
    }


def test_vegetarian_includes_vegan(client):
    res = client.post(
        "/api/recipes/search/",
        {"diet": "vegetarian"},
        format="json",
    )
    assert res.status_code == 200
    names = {r["name"] for r in res.json()}
    assert names == {
        "Tomato Basil Pasta",
        "Tomato Soup",
        "Chickpea Curry",
        "Veggie Stir Fry",
        "Miso Soup",
    }


def test_vegan_only(client):
    res = client.post(
        "/api/recipes/search/",
        {"diet": "vegan"},
        format="json",
    )
    assert res.status_code == 200
    names = {r["name"] for r in res.json()}
    assert names == {"Chickpea Curry", "Miso Soup"}


def test_cuisine_filter(client):
    res = client.post(
        "/api/recipes/search/",
        {"cuisine": "italian"},
        format="json",
    )
    assert res.status_code == 200
    names = {r["name"] for r in res.json()}
    assert names == {"Tomato Basil Pasta", "Basil Pesto Chicken"}


def test_combined_filters(client):
    res = client.post(
        "/api/recipes/search/",
        {
            "ingredients": ["garlic"],
            "diet": "vegetarian",
            "max_cook_time": 30,
            "cuisine": "Italian",
        },
        format="json",
    )
    assert res.status_code == 200
    assert [r["name"] for r in res.json()] == ["Tomato Basil Pasta"]


def test_empty_filters_returns_empty(client):
    res = client.post("/api/recipes/search/", {}, format="json")
    assert res.status_code == 200
    assert res.json() == []


def test_seed_count():
    assert Recipe.objects.count() == 8
