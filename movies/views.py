# movies/views.py
from django.shortcuts import render, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ReviewForm

def home(request):
    # Получаем 10 популярных фильмов, отсортированных по убыванию голосов
    popular_movies = Movie.objects.order_by('-votes')[:10]

    # Получаем 10 новых фильмов, отсортированных по году выпуска
    new_movies = Movie.objects.order_by('-release_year')[:10]

    return render(request, 'movies/home.html', {
        'popular_movies': popular_movies,
        'new_movies': new_movies,
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    return render(request, 'movies/movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return HttpResponseRedirect(reverse('movie_detail', args=[movie_id]))
    else:
        form = ReviewForm()
    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})
