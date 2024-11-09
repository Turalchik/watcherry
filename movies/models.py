# movies/models.py
from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(null=False, default=1900)
    genres = models.ManyToManyField('Genre', related_name='movies')
    actors = models.ManyToManyField('Actor', related_name='movies')
    rating = models.FloatField(null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    title_id = models.CharField(max_length=10, unique=True)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'Review by {self.user} on {self.movie}'
