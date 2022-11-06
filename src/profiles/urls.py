from django.urls import path
from rest_framework.routers import DefaultRouter

from src.profiles import views

urlpatterns = [
    path(r'user/', views.UserView.as_view(
        {'get': 'retrieve', 'put': 'partial_update', 'patch': 'partial_update'}
    ), name="user"),

    path('<int:pk>/', views.UserPublicView.as_view(
        {'get': 'retrieve'}
    ), name="user-pub"),

    path('avatar/', views.UserAvatar.as_view(
        {'put': 'update', 'post': 'create'}
    ), name='user-avatar'),
    path('title/', views.title, name='title'),
    path('done/', views.done, name='done')
]

router = DefaultRouter()
router.register(r'social', views.SocialView, basename='social')
urlpatterns += router.urls
