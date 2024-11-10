# movies/management/commands/populate_movies.py
from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = "Populates the Movie database with test data"

    def handle(self, *args, **options):
        Movie.objects.create(title="Movie 1", description="Description 1", release_year=2023, rating=8.5, votes=1200)
        Movie.objects.create(title="Movie 2", description="Description 2", release_year=2022, rating=7.3, votes=950)
        self.stdout.write(self.style.SUCCESS("Database populated with test movies."))
