from django import forms
from .models import Review, Comment

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