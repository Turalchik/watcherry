from django.contrib import admin
from django.urls import path, include
from movies.views import home

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('admin/', admin.site.urls),
    path('search/', include('search.urls')),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),  # Встроенные маршруты для аутентификации
]
