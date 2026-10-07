from django.db import models


class Recipe(models.Model):
    DIET_ANY = "any"
    DIET_VEGETARIAN = "vegetarian"
    DIET_VEGAN = "vegan"
    DIET_CHOICES = [
        (DIET_ANY, "Any"),
        (DIET_VEGETARIAN, "Vegetarian"),
        (DIET_VEGAN, "Vegan"),
    ]

    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=80)
    ingredients = models.CharField(
        max_length=500, help_text="Comma-separated ingredient list"
    )
    diet = models.CharField(max_length=20, choices=DIET_CHOICES, default=DIET_ANY)
    cook_time_minutes = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name
