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
    
    
class Director(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(null=False, default=1900)
    genres = models.ManyToManyField('Genre', related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    director = models.ForeignKey(Director, on_delete=models.SET_NULL, null=True, related_name='movies')  # Для одного режиссера
    producers = models.ManyToManyField(Producer, related_name='movies')
    rating = models.FloatField(null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    title_id = models.CharField(max_length=10, unique=True)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now) 

    class Meta:
        unique_together = ('user', 'movie')  # Уникальное ограничение: один пользователь - один отзыв на фильм

    def __str__(self):
        return f'Review by {self.user.username} for {self.movie.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user} к отзыву {self.review.id}"