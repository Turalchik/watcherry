# search/models.py
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Actor"
    
    
class Director(models.Model):
    name_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
    

class Writer(models.Model):
    name_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name
    

class Producer(models.Model):
    name_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField(null=False, default=1900)
    genres = models.ManyToManyField('Genre', related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies')
    directors = models.ManyToManyField(Director, related_name='movies') 
    producers = models.ManyToManyField(Producer, related_name='movies')
    writers = models.ManyToManyField(Writer, related_name='movie')
    rating = models.FloatField(null=True, blank=True)
    votes = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    title_id = models.CharField(max_length=10, unique=True)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
