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
    path('add_git_hub/', views.AddGitHub.as_view(), name='add_git_hub'),
    path('git_hub_auth/', views.GitGubAuthView.as_view(), name='git_hub_auth')
]

router = DefaultRouter()
router.register(r'social', views.SocialView, basename='social')
urlpatterns += router.urls
