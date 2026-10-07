"""
Acceptance tests for employee directory search.

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

from employees.models import Employee


@pytest.fixture(autouse=True)
def _db(tmp_path, settings):
    settings.DATABASES["default"]["NAME"] = str(tmp_path / "test.sqlite3")
    call_command("migrate", verbosity=0, interactive=False)
    call_command("seed_employees", verbosity=0)
    return APIClient()


@pytest.fixture
def client(_db):
    return _db


def test_health(client):
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_seed_count():
    assert Employee.objects.count() == 10


def test_department_filter_iexact(client):
    res = client.get("/api/employees/", {"department": "engineering"})
    assert res.status_code == 200
    names = {e["name"] for e in res.json()}
    assert names == {"Alice Chen", "Bob Martinez", "Iris Johansson"}


def test_department_filter_case_insensitive(client):
    res = client.get("/api/employees/", {"department": "SALES"})
    assert res.status_code == 200
    names = {e["name"] for e in res.json()}
    assert names == {"Elena Rossi", "Frank Kim"}


def test_name_search_icontains(client):
    res = client.get("/api/employees/", {"q": "ali"})
    assert res.status_code == 200
    names = {e["name"] for e in res.json()}
    # substring match: Alice Chen, Hassan Ali — not exact full name only
    assert names == {"Alice Chen", "Hassan Ali"}


def test_name_search_partial_middle(client):
    res = client.get("/api/employees/", {"q": "Patel"})
    assert res.status_code == 200
    assert [e["name"] for e in res.json()] == ["Grace Patel"]


def test_sort_by_name_default(client):
    res = client.get("/api/employees/")
    assert res.status_code == 200
    names = [e["name"] for e in res.json()]
    assert names == sorted(names)


def test_sort_by_name_explicit(client):
    res = client.get("/api/employees/", {"sort": "name"})
    assert res.status_code == 200
    names = [e["name"] for e in res.json()]
    assert names == sorted(names)


def test_sort_by_department(client):
    res = client.get("/api/employees/", {"sort": "department"})
    assert res.status_code == 200
    data = res.json()
    departments = [e["department"] for e in data]
    assert departments == sorted(departments)


def test_combined_department_and_q(client):
    res = client.get(
        "/api/employees/",
        {"department": "Engineering", "q": "a"},
    )
    assert res.status_code == 200
    names = {e["name"] for e in res.json()}
    # Engineering with "a" in name: Alice Chen, Bob Martinez, Iris Johansson
    assert names == {"Alice Chen", "Bob Martinez", "Iris Johansson"}
