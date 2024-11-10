# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import ProfileUpdateForm
from .models import Profile
from movies.models import Movie



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
            movie_reviews[movie.id] = review  # Сохраняем целый объект отзыва

    # Если запрос POST, обрабатываем форму для обновления профиля
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    # Добавляем все данные в контекст
    context = {
        'form': form,
        'reviews': reviews,
        'movies_with_reviews': movies_with_reviews,  # Фильмы с отзывами
        'movie_reviews': movie_reviews,  # Словарь с отзывами
    }

    return render(request, 'users/profile.html', context)



