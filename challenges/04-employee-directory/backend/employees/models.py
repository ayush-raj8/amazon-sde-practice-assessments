from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    department = models.CharField(max_length=80)
    job_title = models.CharField(max_length=120)
    location = models.CharField(max_length=120)

    def __str__(self) -> str:
        return f"{self.name} ({self.department})"
