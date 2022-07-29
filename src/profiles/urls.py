from django.urls import path
from src.profiles import views

urlpatterns = [
    path(r'user/<int:pk>/', views.UserFatView.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'
    })),

    path('<int:pk>/', views.UserFatPublicView.as_view({'get': 'retrieve'})),
    path('social/', views.ListSocialView.as_view()),
    path('social/<int:id>/', views.DetailSocialView.as_view()),
]
