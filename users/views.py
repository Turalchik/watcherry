from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from .forms import ProfileUpdateForm
from .models import Profile
from movies.models import Movie
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user

    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    reviews = user.reviews.all()

    movies_with_reviews = Movie.objects.filter(reviews__user=user).distinct()

    movie_reviews = {}
    for movie in movies_with_reviews:
        review = movie.reviews.filter(user=user).first()
        if review:
            movie_reviews[movie] = review.id

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    liked_movies = request.user.profile.liked_movies.all()
    recommendations = get_recommendations(request.user)

    context = {
        'form': form,
        'reviews': reviews,
        'movies_with_reviews': movies_with_reviews,
        'movie_reviews': movie_reviews,
        'liked_movies': liked_movies,
        'recommendations': recommendations,
    }

    return render(request, 'users/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Обновляем хэш сессии
            messages.success(request, "Ваш пароль успешно изменен!")
            return redirect('profile')  # Перенаправление на страницу профиля
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'users/change_password.html', {'form': form})

def get_recommendations(user):
    if not user.is_authenticated:
        return []

    liked_movies = user.profile.liked_movies.prefetch_related('genres', 'actors').all()
    if not liked_movies:
        return []

    liked_genres = set(genre for movie in liked_movies for genre in movie.genres.all())
    liked_actors = set(actor for movie in liked_movies for actor in movie.actors.all())
    liked_producers = set(producer for movie in liked_movies for producer in movie.producers.all())

    filter_criteria = Q()
    if liked_genres:
        filter_criteria |= Q(genres__in=liked_genres)
    if liked_actors:
        filter_criteria |= Q(actors__in=liked_actors)
    if liked_producers:
        filter_criteria |= Q(producers__in=liked_producers)

    if not filter_criteria:
        return []  

    recommendations = Movie.objects.filter(filter_criteria).exclude(id__in=liked_movies).distinct()
    return recommendations
