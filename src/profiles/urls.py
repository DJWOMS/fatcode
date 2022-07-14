from django.urls import path, include
from src.profiles import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
]
