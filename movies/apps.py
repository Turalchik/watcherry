# импортируем класс, от которого мы будем наследоваться, чтобы указать атрибуты name и default_auto_field
# https://docs.djangoproject.com/en/5.1/ref/applications/#application-configuration
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    # теперь тип поля для первичных ключей - BigAutoField
    # наши id являются 64 битными числами, которые автоматически отслеживаются
    default_auto_field = 'django.db.models.BigAutoField'
    # теперь Django обращается к данному приложению как movies
    name = 'movies'
