from django.core.management.base import BaseCommand

from recipes.models import Recipe

RECIPES = [
    {
        "name": "Tomato Basil Pasta",
        "cuisine": "Italian",
        "ingredients": "tomato, basil, garlic, pasta, olive oil",
        "diet": "vegetarian",
        "cook_time_minutes": 25,
    },
    {
        "name": "Tomato Soup",
        "cuisine": "American",
        "ingredients": "tomato, cream, onion, butter",
        "diet": "vegetarian",
        "cook_time_minutes": 20,
    },
    {
        "name": "Basil Pesto Chicken",
        "cuisine": "Italian",
        "ingredients": "basil, chicken, pine nuts, garlic",
        "diet": "any",
        "cook_time_minutes": 35,
    },
    {
        "name": "Chickpea Curry",
        "cuisine": "Indian",
        "ingredients": "chickpea, coconut milk, curry powder, garlic",
        "diet": "vegan",
        "cook_time_minutes": 40,
    },
    {
        "name": "Veggie Stir Fry",
        "cuisine": "Chinese",
        "ingredients": "broccoli, soy sauce, ginger, tofu",
        "diet": "vegetarian",
        "cook_time_minutes": 15,
    },
    {
        "name": "Beef Tacos",
        "cuisine": "Mexican",
        "ingredients": "beef, tortilla, onion, cilantro",
        "diet": "any",
        "cook_time_minutes": 30,
    },
    {
        "name": "Miso Soup",
        "cuisine": "Japanese",
        "ingredients": "miso, tofu, seaweed, green onion",
        "diet": "vegan",
        "cook_time_minutes": 10,
    },
    {
        "name": "Lamb Roast",
        "cuisine": "Mediterranean",
        "ingredients": "lamb, rosemary, garlic, potato",
        "diet": "any",
        "cook_time_minutes": 120,
    },
]


class Command(BaseCommand):
    help = "Seed sample recipes"

    def handle(self, *args, **options):
        Recipe.objects.all().delete()
        for row in RECIPES:
            Recipe.objects.create(**row)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(RECIPES)} recipes"))
