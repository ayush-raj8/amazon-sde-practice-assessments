from datetime import date

from django.core.management.base import BaseCommand

from tasks.models import Task

TASKS = [
    {
        "title": "Write API docs",
        "description": "Document list/create/update endpoints",
        "status": "todo",
        "priority": "medium",
        "due_date": date(2026, 3, 10),
    },
    {
        "title": "Fix login bug",
        "description": "Session cookie not set on Safari",
        "status": "doing",
        "priority": "high",
        "due_date": date(2026, 3, 5),
    },
    {
        "title": "Design smoke tests",
        "description": "Cover health and CRUD happy paths",
        "status": "todo",
        "priority": "low",
        "due_date": date(2026, 3, 20),
    },
    {
        "title": "Ship onboarding email",
        "description": "Welcome template for new users",
        "status": "done",
        "priority": "medium",
        "due_date": date(2026, 2, 28),
    },
    {
        "title": "Refactor filters",
        "description": "Centralize query-param parsing",
        "status": "doing",
        "priority": "medium",
        "due_date": date(2026, 3, 12),
    },
    {
        "title": "Update dependencies",
        "description": "Bump Django and DRF patch versions",
        "status": "todo",
        "priority": "low",
        "due_date": None,
    },
    {
        "title": "Prepare demo script",
        "description": "Walkthrough for stakeholder review",
        "status": "todo",
        "priority": "high",
        "due_date": date(2026, 3, 8),
    },
    {
        "title": "Archive old tickets",
        "description": "Close stale backlog items",
        "status": "done",
        "priority": "low",
        "due_date": date(2026, 3, 1),
    },
]


class Command(BaseCommand):
    help = "Seed sample tasks"

    def handle(self, *args, **options):
        Task.objects.all().delete()
        for row in TASKS:
            Task.objects.create(**row)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(TASKS)} tasks"))
