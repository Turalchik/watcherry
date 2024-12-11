from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from movies.views import MovieListAPIView
from django.conf.urls.static import static

urlpatterns = [
    path('', MovieListAPIView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('', include('movies.urls')),
    path('search/', include('search.urls')),
    path('users/', include('users.urls')),
    path('', include('django.contrib.auth.urls')),
]

#k чтобы аватаарки сохранялись в медиа\аватарс
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)