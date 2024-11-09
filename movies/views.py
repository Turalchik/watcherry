# movies/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ReviewForm
from django.contrib import messages


def home(request):
    # Получаем 10 популярных фильмов, отсортированных по убыванию голосов
    popular_movies = Movie.objects.order_by('-votes')[:10]

    # Получаем 10 новых фильмов, отсортированных по году выпуска
    new_movies = Movie.objects.order_by('-release_year')[:10]

    return render(request, 'movies/home.html', {
        'popular_movies': popular_movies,
        'new_movies': new_movies,
    })


@login_required
def movie_detail(request, title_id):
    movie = Movie.objects.get(title_id=title_id)  # Получаем фильм по title_id

    # Проверяем, есть ли уже отзыв от текущего пользователя
    existing_review = Review.objects.filter(user=request.user, movie=movie).first()

    if request.method == 'POST':
        if existing_review:
            messages.warning(request, "Вы уже оставили отзыв для этого фильма.")
            return redirect('movie_detail', title_id=movie.title_id)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Присваиваем текущего пользователя
            review.movie = movie  # Привязываем отзыв к фильму
            review.save()
            messages.success(request, "Ваш отзыв был добавлен!")
            return redirect('movie_detail', title_id=movie.title_id)
    else:
        form = ReviewForm()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'form': form,
        'existing_review': existing_review  # Передаем существующий отзыв, если он есть
    })

@login_required
def add_review(request, title_id):
    movie = get_object_or_404(Movie, title_id=title_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return HttpResponseRedirect(reverse('movie_detail', args=[title_id]))
    else:
        form = ReviewForm()

    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})


