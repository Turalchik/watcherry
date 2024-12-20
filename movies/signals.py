from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, Movie

@receiver(post_save, sender=Review)
def update_movie_rating(sender, instance, **kwargs):
    movie = instance.movie
    reviews = movie.reviews.all()
    total_votes = reviews.count()
    average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    movie.votes_from_website = total_votes
    movie.rating_from_website = average_rating
    movie.save()
