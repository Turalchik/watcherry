# В Django файл signals.py используется для обработки сигналов,
# которые позволяют выполнять определенные действия в ответ на изменения данных, 
# такие как создание, обновление или удаление объектов в базе данных. 

# users/signals.py
from django.db.models.signals import post_save  # Сигнал, вызываемый после сохранения объекта
from django.dispatch import receiver  # Декоратор для обработки сигналов
from django.contrib.auth.models import User
from .models import Profile

# Функция-сигнал, которая срабатывает при создании нового пользователя
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Создает профиль при создании пользователя

# Функция-сигнал для сохранения профиля
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()  # Сохраняет профиль при изменении пользователя
