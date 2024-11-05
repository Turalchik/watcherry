# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .forms import ProfileUpdateForm
from .models import Profile


@login_required
def profile(request):
    # Создаст страницу profile.html в users/templates/users/
    return render(request, 'users/profile.html')  

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
# Представление для отображения и обновления профиля
def profile(request):
    user = request.user
    # Проверка на наличие профиля, если его нет - создаем
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)

    if request.method == 'POST':  # Если метод POST, значит, пользователь отправил форму
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():  # Проверяем, прошла ли форма валидацию
            form.save()  # Сохраняем изменения
            return redirect('profile')  # Перенаправляем пользователя на страницу профиля
    else:
        form = ProfileUpdateForm(instance=request.user.profile)  # Заполняем форму данными пользователя

    return render(request, 'users/profile.html', {'form': form})
