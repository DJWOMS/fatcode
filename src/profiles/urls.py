from django.urls import path, include
from src.profiles import views

urlpatterns = [
    path('account/registration/', views.RegisterUser.as_view(), name='registration'),
    path('account/login/', views.LoginFormView.as_view(), name='login'),
    path('account/logout/', views.LogoutView.as_view(), name='logout'),
    path('account/profile/', views.ProfileView.as_view(), name='profile'),
]
