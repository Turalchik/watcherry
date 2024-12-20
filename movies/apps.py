# импортируем класс, от которого мы будем наследоваться, чтобы указать атрибуты name и default_auto_field
# https://docs.djangoproject.com/en/5.1/ref/applications/#application-configuration
from django.apps import AppConfig

from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        import movies.signals
