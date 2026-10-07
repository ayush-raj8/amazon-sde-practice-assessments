"""
Acceptance tests for the task manager.

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

from tasks.models import Task


@pytest.fixture(autouse=True)
def _db(tmp_path, settings):
    settings.DATABASES["default"]["NAME"] = str(tmp_path / "test.sqlite3")
    call_command("migrate", verbosity=0, interactive=False)
    call_command("seed_tasks", verbosity=0)
    return APIClient()


@pytest.fixture
def client(_db):
    return _db


def test_health(client):
    res = client.get("/api/health/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_seed_count():
    assert Task.objects.count() == 8


def test_list_all(client):
    res = client.get("/api/tasks/")
    assert res.status_code == 200
    assert len(res.json()) == 8


def test_filter_by_status(client):
    res = client.get("/api/tasks/", {"status": "doing"})
    assert res.status_code == 200
    titles = {t["title"] for t in res.json()}
    assert titles == {"Fix login bug", "Refactor filters"}
    assert all(t["status"] == "doing" for t in res.json())


def test_filter_by_priority(client):
    res = client.get("/api/tasks/", {"priority": "high"})
    assert res.status_code == 200
    titles = {t["title"] for t in res.json()}
    assert titles == {"Fix login bug", "Prepare demo script"}


def test_filter_due_before(client):
    res = client.get("/api/tasks/", {"due_before": "2026-03-08"})
    assert res.status_code == 200
    titles = {t["title"] for t in res.json()}
    # due_date <= 2026-03-08 (null due_date excluded by ORM date comparison)
    assert titles == {
        "Fix login bug",
        "Ship onboarding email",
        "Prepare demo script",
        "Archive old tickets",
    }
    assert "Write API docs" not in titles  # due 2026-03-10
    assert "Design smoke tests" not in titles  # due 2026-03-20


def test_combined_filters(client):
    res = client.get(
        "/api/tasks/",
        {"status": "todo", "priority": "high", "due_before": "2026-03-15"},
    )
    assert res.status_code == 200
    assert [t["title"] for t in res.json()] == ["Prepare demo script"]


def test_create_task(client):
    res = client.post(
        "/api/tasks/",
        {
            "title": "New task",
            "description": "created in test",
            "status": "todo",
            "priority": "low",
            "due_date": "2026-04-01",
        },
        format="json",
    )
    assert res.status_code == 201
    assert res.json()["title"] == "New task"
    assert Task.objects.filter(title="New task").exists()


def test_update_priority(client):
    task = Task.objects.get(title="Write API docs")
    res = client.patch(
        f"/api/tasks/{task.id}/",
        {"priority": "high"},
        format="json",
    )
    assert res.status_code == 200
    assert res.json()["priority"] == "high"
    task.refresh_from_db()
    assert task.priority == "high"


def test_mark_complete_persists(client):
    task = Task.objects.get(title="Fix login bug")
    assert task.status == "doing"
    res = client.post(f"/api/tasks/{task.id}/complete/")
    assert res.status_code == 200
    assert res.json()["status"] == "done"
    task.refresh_from_db()
    assert task.status == "done"


def test_delete_task(client):
    task = Task.objects.get(title="Update dependencies")
    res = client.delete(f"/api/tasks/{task.id}/")
    assert res.status_code == 204
    assert not Task.objects.filter(pk=task.id).exists()
