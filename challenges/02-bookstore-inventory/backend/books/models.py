from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    isbn = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=80)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.title} — {self.author}"
