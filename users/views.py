from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import ProfileUpdateForm
from .models import Profile
from movies.models import Movie
from django.db.models import Q



def register(request):
    if request.method == 'POST':              # 1. Проверка метода запроса
        form = UserCreationForm(request.POST)  # 2. Создание формы с данными
        if form.is_valid():                    # 3. Валидация формы
            user = form.save()                 # 4. Сохранение нового пользователя
            login(request, user)               # 5. Вход нового пользователя
            messages.success(request, 'Регистрация прошла успешно!')  # 6. Сообщение об успехе
            return redirect('profile')         # 7. Перенаправление на профиль
    else:
        form = UserCreationForm()              # 8. Показать пустую форму для GET-запроса
    return render(request, 'registration/register.html', {'form': form})  # 9. Рендер шаблона

@login_required
def profile(request):
    user = request.user

    # Проверка на наличие профиля
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    # Получаем все отзывы пользователя
    reviews = user.reviews.all()

    # Получаем фильмы с отзывами пользователя и сами отзывы
    movies_with_reviews = Movie.objects.filter(reviews__user=user).distinct()

    # Составляем список отзыва каждого фильма пользователя
    movie_reviews = {}
    for movie in movies_with_reviews:
        review = movie.reviews.filter(user=user).first()
        if review:
            movie_reviews[movie] = review.id

    # Если запрос POST, обрабатываем форму для обновления профиля
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    liked_movies = request.user.profile.liked_movies.all()
    recommendations = get_recommendations(request.user)
    
    # Добавляем все данные в контекст
    context = {
        'form': form,
        'reviews': reviews,
        'movies_with_reviews': movies_with_reviews,
        'movie_reviews': movie_reviews,
        'liked_movies': liked_movies,
        'recommendations': recommendations,
    }

    return render(request, 'users/profile.html', context)

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
