# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views
from .views import change_password


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Перенаправление на главную страницу
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', change_password, name='change_password'),

]
