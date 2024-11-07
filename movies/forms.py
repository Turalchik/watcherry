# импортируем данный модуль для доступа к классу для создания форм
from django import forms
# тут просто импортим модель отзыва, которую сами написали в models.py
from .models import Review

# наследуемся от этого класса, который сочетает в себе обычный класс
# для создания форм и класс позволяющий привязываться к моделям
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
