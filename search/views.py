# search/views.py
from django.shortcuts import render
from movies.models import Movie, Genre, Actor

def search_movies(request):
    genre = request.GET.get('genre')
    actor = request.GET.get('actor')
    year = request.GET.get('year')
    rating = request.GET.get('rating')

    movies = Movie.objects.all()

    if genre:
        movies = movies.filter(genres__name__icontains=genre)
    if actor:
        movies = movies.filter(actors__name__icontains=actor)
    if year:
        movies = movies.filter(release_year=year)
    if rating:
        movies = movies.filter(rating__gte=rating)

    return render(request, 'search/search_results.html', {'movies': movies})
