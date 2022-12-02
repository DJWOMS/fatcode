from django.urls import path
from rest_framework.routers import DefaultRouter

from src.profiles import views


urlpatterns = [
    path('users/', views.UsersView.as_view({"get": "list"})),
    path('users/<int:pk>/', views.UsersView.as_view({"get": "retrieve"})),
    path(r'user/', views.UserView.as_view(
        {'get': 'retrieve', 'put': 'partial_update', 'patch': 'partial_update'}
    ), name="user"),

    path('<int:pk>/', views.UserPublicView.as_view({'get': 'retrieve'}), name="user-pub"),

    path('questionnaire/', views.QuestionnaireView.as_view({"get": "list", "post": "create"}), name='questionnaire'),
    path('questionnaire/<int:pk>/', views.QuestionnaireView.as_view(
        {"get": "retrieve", "put": "update", "delete": "destroy"}), name='questionnaire_detail'),
    path('avatar/', views.UserAvatar.as_view(
        {'put': 'update', 'post': 'create'}
    ), name='user-avatar'),
    path('title/', views.title, name='title'),
    path('add_git_hub/', views.AddGitHub.as_view(), name='add_git_hub'),
    path('git_hub_auth/', views.GitGubAuthView.as_view(), name='git_hub_auth'),
    path('application/', views.ApplicationView.as_view({'get': 'list', 'post': 'create'})),
    path('application/<int:pk>/', views.ApplicationView.as_view({'delete': 'destroy'})),
    path('application/to_me', views.ApplicationUserGetterView.as_view({'get': 'list'})),
    path('application/to_me/<int:pk>/', views.ApplicationUserGetterView.as_view({'get': 'retrieve'})),
    path('friend/', views.FriendView.as_view({'get': 'list', 'post': 'create'})),
    path('friend/<int:pk>/', views.FriendView.as_view({'delete': 'destroy'})),
]

router = DefaultRouter()
router.register(r'social', views.SocialView, basename='social')
urlpatterns += router.urls
