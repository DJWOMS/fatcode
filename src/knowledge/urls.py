from django.urls import path
from src.knowledge import views


urlpatterns = [
    path('category/', views.ListCategoryView.as_view()),
    path('category/<int:id>/', views.DetailCategoryView.as_view()),
    path('tag/', views.ListTagView.as_view()),
    path('tag/<int:id>/', views.DetailTagView.as_view()),
    path('article/', views.ListArticleView.as_view()),
    path('article/<int:id>/', views.DetailArticleView.as_view()),
]
