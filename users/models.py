from django.contrib.auth.models import User
from django.db import models
from movies.models import Movie
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    liked_movies = models.ManyToManyField(Movie, related_name='liked_by', blank=True) 

    def __str__(self):
        return f'{self.user.username} Profile'