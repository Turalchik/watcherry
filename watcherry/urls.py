# movie_site/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('search/', include('search.urls')),
    path('users/', include('users.urls')),
]
