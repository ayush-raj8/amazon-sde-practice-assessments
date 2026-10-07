from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=120)
    description = models.TextField()
    cast = models.CharField(max_length=400, help_text="Comma-separated cast names")
    year = models.PositiveIntegerField()
    genre = models.CharField(max_length=80)

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"
