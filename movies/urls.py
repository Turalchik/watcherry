from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie/<str:title_id>/', views.movie_detail, name='movie_detail'),
    path('movie/<str:title_id>/add_review/', views.add_review, name='add_review'),
    path('search/', views.search_movies, name='search_movies'),
]
