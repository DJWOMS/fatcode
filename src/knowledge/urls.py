from django.urls import path

from src.knowledge import views

urlpatterns = [
    path('category/', views.ListCategoryView.as_view(), name='category-list'),
    path('category/<int:id>/', views.DetailCategoryView.as_view(), name='category-detail'),
    path('tag/', views.ListTagView.as_view(), name="tag-list"),
    path('tag/<int:id>/', views.DetailTagView.as_view(), name="tag-detail"),
    path('article/', views.ListArticleView.as_view(), name="article-list"),
    path('article/<int:id>/', views.DetailArticleView.as_view(), name="article-detail"),
]
