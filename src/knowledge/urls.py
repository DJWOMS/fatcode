from django.urls import path

from src.knowledge import views

urlpatterns = [
    path('category/', views.CategoryView.as_view({"get": "list"}), name='category-list'),
    path('article/', views.ArticleView.as_view({"get": "list"}), name="article-list"),
    path('article/<int:pk>/', views.ArticleView.as_view({"get": "retrieve"}), name="article-detail"),
    path('tag/', views.TagListView.as_view(), name="tag-list"),
    path('letters/', views.GlossaryLetterListView.as_view(), name='glossary-letter'),
    path('glossary/', views.GlossaryArticleListView.as_view(), name='glossary-list'),
]
