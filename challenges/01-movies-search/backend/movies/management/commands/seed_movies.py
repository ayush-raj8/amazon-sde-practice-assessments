from django.core.management.base import BaseCommand

from movies.models import Movie

MOVIES = [
    {
        "title": "Inception",
        "director": "Christopher Nolan",
        "description": "A thief who steals corporate secrets through dream-sharing technology.",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",
        "year": 2010,
        "genre": "Sci-Fi",
    },
    {
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "description": "Batman faces the Joker in Gotham City.",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "year": 2008,
        "genre": "Action",
    },
    {
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "description": "Explorers travel through a wormhole in space to save humanity.",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "year": 2014,
        "genre": "Sci-Fi",
    },
    {
        "title": "Pulp Fiction",
        "director": "Quentin Tarantino",
        "description": "The lives of two mob hitmen, a boxer, and others intertwine.",
        "cast": "John Travolta, Samuel L. Jackson, Uma Thurman",
        "year": 1994,
        "genre": "Crime",
    },
    {
        "title": "The Matrix",
        "director": "Lana Wachowski",
        "description": "A computer hacker learns about the true nature of reality.",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "year": 1999,
        "genre": "Sci-Fi",
    },
    {
        "title": "Spirited Away",
        "director": "Hayao Miyazaki",
        "description": "A girl enters a world of spirits ruled by gods and witches.",
        "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki",
        "year": 2001,
        "genre": "Animation",
    },
    {
        "title": "Parasite",
        "director": "Bong Joon-ho",
        "description": "A poor family schemes to become employed by a wealthy household.",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "year": 2019,
        "genre": "Thriller",
    },
    {
        "title": "Arrival",
        "director": "Denis Villeneuve",
        "description": "A linguist works with the military to communicate with aliens.",
        "cast": "Amy Adams, Jeremy Renner, Forest Whitaker",
        "year": 2016,
        "genre": "Sci-Fi",
    },
]


class Command(BaseCommand):
    help = "Seed sample movies"

    def handle(self, *args, **options):
        Movie.objects.all().delete()
        for row in MOVIES:
            Movie.objects.create(**row)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(MOVIES)} movies"))
