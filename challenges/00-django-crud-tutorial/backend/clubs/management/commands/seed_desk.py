from datetime import date, timedelta

from django.core.management.base import BaseCommand

from clubs.models import Club
from events.models import Event

CLUBS = [
    {"name": "Robotics", "campus": "North", "category": "STEM", "member_count": 42},
    {"name": "Chess", "campus": "South", "category": "Games", "member_count": 18},
    {"name": "Drama", "campus": "North", "category": "Arts", "member_count": 30},
    {"name": "Hiking", "campus": "East", "category": "Outdoors", "member_count": 25},
    {"name": "Coding", "campus": "West", "category": "STEM", "member_count": 55},
    {"name": "Photography", "campus": "South", "category": "Arts", "member_count": 22},
]


class Command(BaseCommand):
    help = "Seed clubs and events for the CRUD tutorial"

    def handle(self, *args, **options):
        Event.objects.all().delete()
        Club.objects.all().delete()

        clubs = {row["name"]: Club.objects.create(**row) for row in CLUBS}
        today = date.today()

        events = [
            {
                "title": "Bot Build Night",
                "club": clubs["Robotics"],
                "event_date": today + timedelta(days=3),
                "location": "Lab A",
                "capacity": 40,
                "status": "scheduled",
            },
            {
                "title": "Blitz Tournament",
                "club": clubs["Chess"],
                "event_date": today + timedelta(days=7),
                "location": "Student Center",
                "capacity": 32,
                "status": "scheduled",
            },
            {
                "title": "Spring Showcase",
                "club": clubs["Drama"],
                "event_date": today + timedelta(days=14),
                "location": "Auditorium",
                "capacity": 200,
                "status": "scheduled",
            },
            {
                "title": "Trail Cleanup",
                "club": clubs["Hiking"],
                "event_date": today + timedelta(days=5),
                "location": "East Gate",
                "capacity": 20,
                "status": "scheduled",
            },
            {
                "title": "Hack Night",
                "club": clubs["Coding"],
                "event_date": today + timedelta(days=2),
                "location": "CS Lounge",
                "capacity": 50,
                "status": "scheduled",
            },
            {
                "title": "Golden Hour Walk",
                "club": clubs["Photography"],
                "event_date": today + timedelta(days=10),
                "location": "River Path",
                "capacity": 15,
                "status": "scheduled",
            },
            {
                "title": "Sensor Workshop",
                "club": clubs["Robotics"],
                "event_date": today + timedelta(days=21),
                "location": "Lab B",
                "capacity": 25,
                "status": "scheduled",
            },
            {
                "title": "Algo Study Group",
                "club": clubs["Coding"],
                "event_date": today + timedelta(days=4),
                "location": "Library 3F",
                "capacity": 16,
                "status": "scheduled",
            },
        ]
        for row in events:
            Event.objects.create(**row)

        self.stdout.write(
            self.style.SUCCESS(f"Seeded {len(CLUBS)} clubs and {len(events)} events")
        )
