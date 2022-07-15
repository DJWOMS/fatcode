from django.urls import path, include
from src.profiles import views

urlpatterns = [
    path('profile/<int:pk>/', views.UserFatView.as_view({'get': 'retrieve',
                                                         'put': 'update'})),

    path('<int:pk>/', views.UserFatPublicView.as_view({'get': 'retrieve'})),
]
