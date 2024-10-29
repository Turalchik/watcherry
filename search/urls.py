# search/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_movies, name='search_movies'),
]
