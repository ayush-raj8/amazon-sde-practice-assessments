"""
Acceptance tests for movie search.

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

from movies.models import Movie


@pytest.fixture(autouse=True)
def _db(tmp_path, settings):
    settings.DATABASES["default"]["NAME"] = str(tmp_path / "test.sqlite3")
    call_command("migrate", verbosity=0, interactive=False)
    call_command("seed_movies", verbosity=0)
    return APIClient()


@pytest.fixture
def client(_db):
    return _db


def test_health(client):
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_simple_search_by_director(client):
    res = client.get("/api/movies/search/", {"q": "Nolan", "field": "director"})
    assert res.status_code == 200
    titles = {m["title"] for m in res.json()}
    assert titles == {"Inception", "The Dark Knight", "Interstellar"}


def test_simple_search_by_cast(client):
    res = client.get("/api/movies/search/", {"q": "Keanu", "field": "cast"})
    assert res.status_code == 200
    titles = {m["title"] for m in res.json()}
    assert titles == {"The Matrix"}


def test_simple_search_by_description(client):
    res = client.get("/api/movies/search/", {"q": "wormhole", "field": "description"})
    assert res.status_code == 200
    assert [m["title"] for m in res.json()] == ["Interstellar"]


def test_simple_search_all_fields(client):
    res = client.get("/api/movies/search/", {"q": "dream", "field": "all"})
    assert res.status_code == 200
    titles = {m["title"] for m in res.json()}
    assert "Inception" in titles


def test_simple_search_title_still_works(client):
    res = client.get("/api/movies/search/", {"q": "Parasite", "field": "title"})
    assert res.status_code == 200
    assert [m["title"] for m in res.json()] == ["Parasite"]


def test_advanced_search_ands_filters(client):
    res = client.post(
        "/api/movies/advanced-search/",
        {"director": "Nolan", "genre": "Sci-Fi"},
        format="json",
    )
    assert res.status_code == 200
    titles = {m["title"] for m in res.json()}
    # Must be AND: Nolan Sci-Fi only (not Dark Knight / Action)
    assert titles == {"Inception", "Interstellar"}


def test_advanced_search_three_dimensions(client):
    res = client.post(
        "/api/movies/advanced-search/",
        {"genre": "Sci-Fi", "cast": "Keanu", "year": 1999},
        format="json",
    )
    assert res.status_code == 200
    assert [m["title"] for m in res.json()] == ["The Matrix"]


def test_advanced_search_empty_filters_returns_empty(client):
    res = client.post("/api/movies/advanced-search/", {}, format="json")
    assert res.status_code == 200
    assert res.json() == []


def test_seed_count():
    assert Movie.objects.count() == 8
