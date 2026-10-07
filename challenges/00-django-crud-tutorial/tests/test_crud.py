"""
Acceptance tests for Campus Club Desk CRUD tutorial.

Fail on buggy starter code; pass once settings/URL/view behavior matches the README.
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

from clubs.models import Club
from events.models import Event


@pytest.fixture(autouse=True)
def _db(tmp_path, settings):
    settings.DATABASES["default"]["NAME"] = str(tmp_path / "test.sqlite3")
    call_command("migrate", verbosity=0, interactive=False)
    call_command("seed_desk", verbosity=0)
    return APIClient()


@pytest.fixture
def client(_db):
    return _db


def test_health(client):
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_seed_counts():
    assert Club.objects.count() == 6
    assert Event.objects.count() == 8


def test_list_clubs(client):
    res = client.get("/api/clubs/")
    assert res.status_code == 200
    assert len(res.json()) == 6


def test_club_category_filter(client):
    res = client.get("/api/clubs/", {"category": "stem"})
    assert res.status_code == 200
    names = {c["name"] for c in res.json()}
    assert names == {"Robotics", "Coding"}


def test_create_club(client):
    res = client.post(
        "/api/clubs/",
        {
            "name": "Debate",
            "campus": "North",
            "category": "Academic",
            "member_count": 12,
        },
        format="json",
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Debate"
    assert Club.objects.count() == 7


def test_update_campus_persists(client):
    club = Club.objects.get(name="Chess")
    res = client.patch(
        f"/api/clubs/{club.id}/",
        {"campus": "West"},
        format="json",
    )
    assert res.status_code == 200
    club.refresh_from_db()
    assert club.campus == "West"
    assert res.json()["campus"] == "West"


def test_delete_club(client):
    club = Club.objects.get(name="Photography")
    res = client.delete(f"/api/clubs/{club.id}/")
    assert res.status_code == 204
    assert not Club.objects.filter(id=club.id).exists()


def test_list_events(client):
    res = client.get("/api/events/")
    assert res.status_code == 200
    assert len(res.json()) == 8


def test_events_filter_by_club(client):
    robotics = Club.objects.get(name="Robotics")
    res = client.get("/api/events/", {"club": robotics.id})
    assert res.status_code == 200
    titles = {e["title"] for e in res.json()}
    assert titles == {"Bot Build Night", "Sensor Workshop"}
    assert all(e["club"] == robotics.id for e in res.json())


def test_create_event(client):
    chess = Club.objects.get(name="Chess")
    res = client.post(
        "/api/events/",
        {
            "title": "Open Board Night",
            "club": chess.id,
            "event_date": "2030-06-01",
            "location": "Cafe",
            "capacity": 10,
            "status": "scheduled",
        },
        format="json",
    )
    assert res.status_code == 201
    assert res.json()["title"] == "Open Board Night"
    assert Event.objects.count() == 9


def test_cancel_event_persists(client):
    event = Event.objects.get(title="Hack Night")
    res = client.post(f"/api/events/{event.id}/cancel/")
    assert res.status_code == 200
    event.refresh_from_db()
    assert event.status == "cancelled"
    assert res.json()["status"] == "cancelled"


def test_delete_event(client):
    event = Event.objects.get(title="Trail Cleanup")
    res = client.delete(f"/api/events/{event.id}/")
    assert res.status_code == 204
    assert not Event.objects.filter(id=event.id).exists()
