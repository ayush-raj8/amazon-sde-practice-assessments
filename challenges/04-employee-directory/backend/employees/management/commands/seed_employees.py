from django.core.management.base import BaseCommand

from employees.models import Employee

# Intentionally not inserted in name order so buggy order_by("id") fails sort tests.
EMPLOYEES = [
    {
        "name": "Jamal Wright",
        "email": "jamal.wright@example.com",
        "department": "Marketing",
        "job_title": "Content Strategist",
        "location": "New York",
    },
    {
        "name": "Elena Rossi",
        "email": "elena.rossi@example.com",
        "department": "Sales",
        "job_title": "Account Executive",
        "location": "Chicago",
    },
    {
        "name": "Bob Martinez",
        "email": "bob.martinez@example.com",
        "department": "Engineering",
        "job_title": "Senior Software Engineer",
        "location": "Austin",
    },
    {
        "name": "Iris Johansson",
        "email": "iris.johansson@example.com",
        "department": "Engineering",
        "job_title": "Engineering Manager",
        "location": "Stockholm",
    },
    {
        "name": "Carla Nguyen",
        "email": "carla.nguyen@example.com",
        "department": "Product",
        "job_title": "Product Manager",
        "location": "Seattle",
    },
    {
        "name": "Hassan Ali",
        "email": "hassan.ali@example.com",
        "department": "HR",
        "job_title": "Recruiter",
        "location": "Remote",
    },
    {
        "name": "Alice Chen",
        "email": "alice.chen@example.com",
        "department": "Engineering",
        "job_title": "Software Engineer",
        "location": "Seattle",
    },
    {
        "name": "Frank Kim",
        "email": "frank.kim@example.com",
        "department": "Sales",
        "job_title": "Sales Engineer",
        "location": "San Francisco",
    },
    {
        "name": "Grace Patel",
        "email": "grace.patel@example.com",
        "department": "HR",
        "job_title": "HR Business Partner",
        "location": "Austin",
    },
    {
        "name": "David Okonkwo",
        "email": "david.okonkwo@example.com",
        "department": "Product",
        "job_title": "Product Designer",
        "location": "New York",
    },
]


class Command(BaseCommand):
    help = "Seed sample employees"

    def handle(self, *args, **options):
        Employee.objects.all().delete()
        for row in EMPLOYEES:
            Employee.objects.create(**row)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(EMPLOYEES)} employees"))
