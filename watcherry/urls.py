from django.contrib import admin
from django.urls import path, include
from movies.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('search/', include('search.urls')),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),  # Встроенные маршруты для аутентификации
]

#k чтобы аватаарки сохранялись в медиа\аватарс
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)