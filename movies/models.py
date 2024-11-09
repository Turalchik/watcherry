# movies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')  # Связь с пользователем
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Связь с фильмом
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 

    class Meta:
        unique_together = ('user', 'movie')  # Уникальное ограничение: один пользователь - один отзыв на фильм

    def __str__(self):
        return f'Review by {self.user.username} for {self.movie.title}'
