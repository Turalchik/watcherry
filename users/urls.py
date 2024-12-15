from django.urls import path
from .views import (
    LoginView, RegisterAPIView, ProfileAPIView,
    ChangePasswordAPIView, RecommendationsAPIView
)

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/profile/', ProfileAPIView.as_view(), name='api-profile'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='api-change-password'),
    path('api/recommendations/', RecommendationsAPIView.as_view(), name='api-recommendations'),
]
