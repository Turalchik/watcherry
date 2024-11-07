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
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    rating = models.FloatField(default=0.0)
    votes = models.IntegerField(default=0)
    title_id = models.CharField(max_length=20)
    poster_url = models.URLField(max_length=500, null=True, blank=True)  # Поле для URL постера

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f'Review by {self.user} on {self.movie}'
