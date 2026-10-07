"""
Acceptance tests for bookstore inventory.

These fail on the buggy starter code and pass once the candidate fixes behavior.
"""

import os
import sys
from decimal import Decimal

import pytest

BACKEND = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, BACKEND)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.core.management import call_command
from rest_framework.test import APIClient

from books.models import Book


@pytest.fixture(autouse=True)
def _db(tmp_path, settings):
    settings.DATABASES["default"]["NAME"] = str(tmp_path / "test.sqlite3")
    call_command("migrate", verbosity=0, interactive=False)
    call_command("seed_books", verbosity=0)
    return APIClient()


@pytest.fixture
def client(_db):
    return _db


def test_health(client):
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_seed_count():
    assert Book.objects.count() == 8


def test_list_books(client):
    res = client.get("/api/books/")
    assert res.status_code == 200
    assert len(res.json()) == 8


def test_create_book(client):
    res = client.post(
        "/api/books/",
        {
            "title": "New Title",
            "author": "New Author",
            "isbn": "9780000000001",
            "price": "11.11",
            "category": "Mystery",
            "stock": 3,
        },
        format="json",
    )
    assert res.status_code == 201
    assert res.json()["title"] == "New Title"
    assert Book.objects.count() == 9


def test_update_price_persists(client):
    book = Book.objects.get(title="Dune")
    original = book.price
    res = client.patch(
        f"/api/books/{book.id}/",
        {"price": "99.99"},
        format="json",
    )
    assert res.status_code == 200
    book.refresh_from_db()
    assert book.price == Decimal("99.99")
    assert book.price != original
    assert Decimal(str(res.json()["price"])) == Decimal("99.99")


def test_category_filter_works(client):
    res = client.get("/api/books/", {"category": "sci-fi"})
    assert res.status_code == 200
    titles = {b["title"] for b in res.json()}
    assert titles == {"Dune", "Foundation", "Neuromancer"}


def test_category_filter_exact_case_insensitive(client):
    res = client.get("/api/books/", {"category": "FANTASY"})
    assert res.status_code == 200
    titles = {b["title"] for b in res.json()}
    assert titles == {"The Hobbit", "The Name of the Wind"}


def test_q_matches_author(client):
    res = client.get("/api/books/", {"q": "Tolkien"})
    assert res.status_code == 200
    assert [b["title"] for b in res.json()] == ["The Hobbit"]


def test_q_matches_title(client):
    res = client.get("/api/books/", {"q": "Sapiens"})
    assert res.status_code == 200
    assert [b["title"] for b in res.json()] == ["Sapiens"]


def test_delete_book(client):
    book = Book.objects.get(title="Educated")
    res = client.delete(f"/api/books/{book.id}/")
    assert res.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()
