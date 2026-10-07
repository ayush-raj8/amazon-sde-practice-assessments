from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "Todo"),
        ("doing", "Doing"),
        ("done", "Done"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="todo")
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title} [{self.status}]"
