from django.urls import path
from .views import (
    LoginView, RegisterAPIView, ProfileAPIView,
    ChangePasswordAPIView, RecommendationsAPIView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('profile/', ProfileAPIView.as_view(), name='api-profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='api-change-password'),
    path('recommendations/', RecommendationsAPIView.as_view(), name='api-recommendations'),
]
