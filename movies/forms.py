# импортируем данный модуль для доступа к классу для создания форм
from django import forms
# тут просто импортим модель отзыва, которую сами написали в models.py
from .models import Review, Comment

# наследуемся от этого класса, который сочетает в себе обычный класс
# для создания форм и класс позволяющий привязываться к моделям
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10, 'step': 1}),  # Ограничения для рейтинга
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']