# users/forms.py
from django import forms
from .models import Profile

# Форма для обновления профиля пользователя
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile  # Модель, на которой основана форма
        fields = ['avatar']  # Поля для редактирования
