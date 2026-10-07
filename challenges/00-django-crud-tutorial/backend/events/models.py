from django.db import models


class Event(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    title = models.CharField(max_length=160)
    club = models.ForeignKey("clubs.Club", on_delete=models.CASCADE, related_name="events")
    event_date = models.DateField()
    location = models.CharField(max_length=120)
    capacity = models.PositiveIntegerField(default=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")

    def __str__(self) -> str:
        return self.title
