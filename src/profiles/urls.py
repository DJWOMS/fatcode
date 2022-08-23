from django.urls import path
from rest_framework.routers import DefaultRouter

from src.profiles import views

urlpatterns = [
    path(r'user/<int:pk>/', views.UserView.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'
    })),

    path('<int:pk>/', views.UserPublicView.as_view({'get': 'retrieve'}))
]

router = DefaultRouter()
router.register(r'social', views.SocialView, basename='social')
urlpatterns += router.urls
