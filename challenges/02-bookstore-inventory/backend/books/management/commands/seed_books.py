from decimal import Decimal

from django.core.management.base import BaseCommand

from books.models import Book

BOOKS = [
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "isbn": "9780547928227",
        "price": Decimal("14.99"),
        "category": "Fantasy",
        "stock": 12,
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "isbn": "9780441172719",
        "price": Decimal("16.50"),
        "category": "Sci-Fi",
        "stock": 8,
    },
    {
        "title": "Foundation",
        "author": "Isaac Asimov",
        "isbn": "9780553293357",
        "price": Decimal("12.00"),
        "category": "Sci-Fi",
        "stock": 5,
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "isbn": "9780141439518",
        "price": Decimal("9.99"),
        "category": "Classic",
        "stock": 20,
    },
    {
        "title": "Neuromancer",
        "author": "William Gibson",
        "isbn": "9780441569595",
        "price": Decimal("13.25"),
        "category": "Sci-Fi",
        "stock": 4,
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "isbn": "9780756404741",
        "price": Decimal("18.00"),
        "category": "Fantasy",
        "stock": 7,
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "isbn": "9780399590504",
        "price": Decimal("15.00"),
        "category": "Memoir",
        "stock": 10,
    },
    {
        "title": "Sapiens",
        "author": "Yuval Noah Harari",
        "isbn": "9780062316097",
        "price": Decimal("17.50"),
        "category": "Nonfiction",
        "stock": 15,
    },
]


class Command(BaseCommand):
    help = "Seed sample books"

    def handle(self, *args, **options):
        Book.objects.all().delete()
        for row in BOOKS:
            Book.objects.create(**row)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(BOOKS)} books"))
